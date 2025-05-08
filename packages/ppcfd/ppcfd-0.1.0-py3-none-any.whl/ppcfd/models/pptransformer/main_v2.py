import logging
import os
import time

import hydra
import numpy as np
import paddle
import paddle.distributed as dist
import pandas as pd
import tensorboardX
import warp
from paddle.distributed import fleet

from src.data import instantiate_datamodule
from src.networks import instantiate_network
from src.utils.loss import LpLoss
from src.utils.mp import init_dist_env
from src.utils.mp import parallelize
from src.utils.mp import replicate_data_dict
from src.utils.mp import shard_data_dict

log = logging.getLogger(__name__)
tensorboard = None


def set_seed(seed: int = 0):
    paddle.seed(seed)
    np.random.seed(seed)
    warp.rand_init(seed)


def integral_over_cells(
    reference_area,
    surface_normals,
    areas,
    mass_density,
    flow_speed,
    x_direction=1,
):
    flow_normals = paddle.zeros(surface_normals.shape)
    flow_normals[:, 0] = x_direction
    const = 2.0 / (mass_density * flow_speed**2 * reference_area)
    direction = paddle.sum(surface_normals * flow_normals, axis=1, keepdim=False)
    c_p = const * direction * areas
    c_f = (const * flow_normals * areas[:, None])[:, 0]
    return c_p, c_f


def calculate_coefficient(
    data_dict,
    p_pred,
    p_true,
    wss_x_pred,
    wss_x_true,
    mass_density,
    flow_speed,
    x_direction=1,
):
    if "Cd" not in data_dict:
        data_dict["Cd"] = paddle.to_tensor(0.0)

    if p_pred is None:
        return [paddle.zeros([1])]*12
    else:
        if isinstance(data_dict["Cd"], list):
            data_dict["Cd"] = data_dict["Cd"][0]
    # 1. load data TODO:load from test_data not from data_path
    reference_area = data_dict["reference_area"]
    reference_area = (
        reference_area[0] if isinstance(reference_area, list) else reference_area.item()
    )
    surface_normal = data_dict["normal"][0]
    areas = data_dict["areas"][0]

    # 2. Prepare Discreted Integral over Car Surface
    assert len(surface_normal.shape) == 2 and surface_normal.shape[1] == 3
    assert len(areas.shape) == 1 and areas.shape[0] == surface_normal.shape[0]
    cp, cf = integral_over_cells(
        reference_area,
        surface_normal,
        areas,
        mass_density,
        flow_speed,
        x_direction,
    )
    # 3. Calculate coefficient and MRE
    c_p_pred = paddle.sum(cp * p_pred.reshape([-1])) if p_pred is not None else 1e-5
    c_p_true = paddle.sum(cp * p_true.reshape([-1])) if p_true is not None else 1e-5
    c_p_mre = abs(c_p_pred - c_p_true) / abs(c_p_true)

    c_f_pred = (
        paddle.sum(cf * wss_x_pred.reshape([-1])) if wss_x_pred is not None else 1e-5
    )
    c_f_true = (
        paddle.sum(cf * wss_x_true.reshape([-1])) if wss_x_true is not None else 1e-5
    )
    c_f_mre = abs(c_f_pred - c_f_true) / abs(c_f_true)

    c_d_pred = c_p_pred + c_f_pred
    c_d_true = c_p_true + c_f_true
    c_d_mre = abs(c_d_pred - c_d_true) / abs(c_d_true)
    c_d_mre = c_d_mre

    c_l_pred = 1.0  # TODO: calculate c_l_pred and c_l_true
    c_l_true = 1.0
    c_l_mre = abs(c_l_pred - c_l_true) / abs(c_l_true)
    coefficient = (
        c_p_pred,
        c_p_true,
        c_p_mre,
        c_f_pred,
        c_f_true,
        c_f_mre,
        c_d_pred,
        c_d_true,
        c_d_mre,
        c_l_pred,
        c_l_true,
        c_l_mre,
    )
    coefficient = [paddle.to_tensor(c) for c in coefficient]
    return coefficient


def load_checkpoint(config, model):
    """
    加载模型检查点（checkpoint）并应用到模型中。

    Args:
        config (Config): 配置对象，包含检查点的路径等信息。
        model (nn.Module): 要加载检查点的模型对象。

    Returns:
        None

    Raises:
        AssertionError: 如果配置中没有提供检查点路径，将抛出断言错误。
    """
    assert config.checkpoint is not None, "checkpoint must be given."
    checkpoint = paddle.load(f"{config.checkpoint}.pdparams")
    if "model_state_dict" in checkpoint:
        model.set_state_dict(checkpoint["model_state_dict"])
    else:
        model.set_state_dict(checkpoint)


def denormalize(config, data_dict, output, mode):
    channels = 0
    label_list, pred_list = [], []
    p_true, p_pred, wss_true, wss_pred, wss_x_true, wss_x_pred, vel_true, vel_pred = [
        None
    ] * 8
    if "pressure" in config.out_keys:
        if mode in ["test", "train"]:
            p_true = data_dict["pressure"].unsqueeze(axis=2)
            label_list.append(p_true)
        mean = data_dict["p_mean"][0]
        std = data_dict["p_std"][0]
        index = config.out_keys.index("pressure")
        n = config.out_channels[index]
        p_pred = output[..., channels : channels + n] * mean + std
        pred_list.append(p_pred)
        channels += n

    if "wss" in config.out_keys:
        if mode in ["test", "train"]:
            wss_true = data_dict["wss"]
            label_list.append(wss_true)
            wss_x_true = wss_true[0, :, 0]
        mean = data_dict["wss_mean"][0]
        std = data_dict["wss_std"][0]
        index = config.out_keys.index("wss")
        n = config.out_channels[index]
        wss_pred = output[..., channels : channels + n] * mean + std
        wss_x_pred = wss_pred[0, :, 0]
        pred_list.append(wss_pred)
        channels += n

    if "vel" in config.out_keys:
        if mode in ["test", "train"]:
            vel_true = data_dict["vel"].unsqueeze(axis=2)
            label_list.append(vel_true)
        mean = data_dict["v_mean"][0]
        std = data_dict["v_std"][0]
        index = config.out_keys.index("vel")
        n = config.out_channels[index]
        vel_pred = output[..., channels : channels + n] * mean + std
        pred_list.append(vel_pred)
        channels += n

    pred_list = paddle.concat(pred_list, axis=-1)
    if mode in ["test", "train"]:
        label_list = paddle.concat(label_list, axis=-1)
    return [pred_list, label_list], [
        p_true,
        p_pred,
        wss_true,
        wss_pred,
        wss_x_true,
        wss_x_pred,
        vel_true,
        vel_pred,
    ]


# 非常复杂的计算，建议别看
def car_loss(config, output, data, loss_fn, loss_cd_fn):
    l2_loss, mse_cd_loss, c_p_mre, loss_p, loss_wss, loss_vel = [0.0] * 6
    [output, label], [
        p_true,
        p_pred,
        wss_true,
        wss_pred,
        wss_x_true,
        wss_x_pred,
        vel_true,
        vel_pred,
    ] = denormalize(config, data, output, config.mode)
    data["coefficient"] = calculate_coefficient(
        data,
        p_pred,
        p_true,
        wss_x_pred,
        wss_x_true,
        config.mass_density,
        config.flow_speed,
    )
    # 解包系数
    (
        c_p_pred,
        c_p_true,
        c_p_mre,
        c_f_pred,
        c_f_true,
        c_f_mre,
        c_d_pred,
        c_d_true,
        c_d_mre,
        c_l_pred,
        c_l_true,
        c_l_mre,
    ) = data["coefficient"]
    # 根据配置提取相关值
    if "pressure" in config.out_keys:
        loss_p = loss_fn(p_true, p_pred)

    if "wss" in config.out_keys:
        loss_wss = loss_fn(wss_true, wss_pred)

    if "vel" in config.out_keys:
        loss_vel = loss_fn(vel_true, vel_pred)

    l2_loss = loss_fn(output, label)

    if config.cd_finetune is True:
        mse_cd_loss = loss_cd_fn(c_p_pred, c_p_true)
    else:
        mse_cd_loss = 0.0
    return_list = (
        l2_loss,
        mse_cd_loss,
        loss_p,
        loss_wss,
        loss_vel,
        c_p_mre,
        c_f_mre,
        c_d_mre,
        c_l_mre,
    )
    return_list = [
        paddle.to_tensor([x]) if isinstance(x, float) else x for x in return_list
    ]
    return return_list


def load_checkpoint(config, model):
    assert config.checkpoint is not None, "checkpoint must be given."
    checkpoint = paddle.load(f"{config.checkpoint}.pdparams")
    if "model_state_dict" in checkpoint:
        model.set_state_dict(checkpoint["model_state_dict"])
    else:
        model.set_state_dict(checkpoint)


def log_and_tensorboard(
    config,
    ep,
    time_cost,
    lr,
    train_loss_list_p,
    train_loss_list_cd,
    train_cp_mre_list,
    test_l2_loss_list,
    test_mse_cd_loss_list,
    test_cp_mre_list,
    test_cf_mre_list,
):
    global tensorboard
    tensorboard.add_scalar("[Tain] [Physics  L2]  loss", np.mean(train_loss_list_p), ep)
    tensorboard.add_scalar(
        "[Tain] [Cd coeff MSE] loss", np.mean(train_loss_list_cd), ep
    )
    tensorboard.add_scalar("[Test] [Physics  L2]  loss", np.mean(test_l2_loss_list), ep)
    tensorboard.add_scalar("[Test] [Cd coeff MRE] loss", np.mean(test_l2_loss_list), ep)
    log.info(
        f"Epoch {ep}  Times {(time_cost):.2f}s, lr:{lr:.1e}, [Tain] L2 loss:{np.mean(train_loss_list_p):.4f}, Cd MSE Loss:{np.mean(train_loss_list_cd):.1e},  Cp MRE:{100*np.mean(train_cp_mre_list):.4f}%   [Test] L2 loss:{np.mean(test_l2_loss_list):.4f}, Cd loss:{np.mean(test_mse_cd_loss_list):.1e}, Cp MRE:{100*np.mean(test_cp_mre_list):.4f}%, Cf MRE:{100*np.mean(test_cf_mre_list):.4f}%"
    )


@paddle.no_grad()
def test(config, model, test_data, device):
    model.eval()
    if config.mode == "test":
        load_checkpoint(config, model)
    loss_fn = LpLoss(size_average=True)
    loss_cd_fn = paddle.nn.MSELoss()
    loss_p, loss_wss, loss_vel = 0.0, 0.0, 0.0
    cd_list = [["file_name", "cp pred", "cf pred", "cp true", "cf true", "cd starccm+"]]
    (
        test_l2_loss_list,
        test_mse_cd_loss_list,
        test_loss_p,
        test_loss_wss,
        test_loss_vel,
    ) = ([], [], [], [], [])
    test_cp_mre_list, test_cf_mre_list, test_loss_cd, test_loss_cl = [], [], [], []

    if config.enable_mp or config.enable_pp:
        init_dist_env(config)
        model, _ = parallelize(model, None, config)

    for i, data in enumerate(test_data):
        if config.enable_mp:
            data = shard_data_dict(
                data,
                shard_dim=1,
                ignore_keys=[
                    "file_name",
                    "p_mean",
                    "p_std",
                    "wss_mean",
                    "wss_std",
                    "reference_area",
                ],
            )
        output = model(data)
        if config.enable_mp:
            data = replicate_data_dict(data)
        elif config.enable_pp:
            mesh = dist.ProcessMesh(
                np.arange(0, paddle.distributed.get_world_size()), dim_names=["x"]
            )
            output = dist.reshard(output, mesh, [dist.Replicate()])
        (
            l2_loss,
            mse_cd_loss,
            loss_p,
            loss_wss,
            loss_vel,
            c_p_mre,
            c_f_mre,
            c_d_mre,
            c_l_mre,
        ) = car_loss(config, output, data, loss_fn, loss_cd_fn)
        # 将损失和系数添加到相应的列表中
        test_l2_loss_list.append(l2_loss.item())
        test_mse_cd_loss_list.append(mse_cd_loss.item())
        test_cp_mre_list.append(c_p_mre.item())
        test_cf_mre_list.append(c_f_mre.item())
        test_loss_p.append(loss_p.item())
        test_loss_wss.append(loss_wss.item())
        test_loss_vel.append(loss_vel.item())
        test_loss_cd.append(c_d_mre.item())
        test_loss_cl.append(c_l_mre.item())
        log.info(
            f"Case {data['file_name']}\t MRE Error : [Cp], {c_p_mre.item()*100:.2f}%, [Cf], {c_f_mre.item()*100:.2f}%, [Cd], {c_d_mre.item()*100:.2f}%, [Cl], {c_l_mre.item()*100:.2f}% \tRelative L2 Error : [P], {loss_p.item():.4f}, [WSS], {loss_wss.item():.4f}, [VEL], {loss_vel.item():.4f}"
        )
        c_p_pred = data["coefficient"][0]
        c_p_true = data["coefficient"][1]
        c_f_pred = data["coefficient"][3]
        c_f_true = data["coefficient"][4]
        c_d_pred = data["coefficient"][6]
        c_d_true = data["coefficient"][7]
        cd_list.append(
            [
                data["file_name"],
                c_p_pred.item(),
                c_f_pred.item(),
                c_p_true.item(),
                c_f_true.item(),
                data["Cd"].item(),
            ]
        )

    # 将二维列表转换为 pandas DataFrame
    df = pd.DataFrame(cd_list[1:], columns=cd_list[0])
    # 使用 DataFrame 的 to_csv 方法将二维列表保存为 CSV 文件
    df.to_csv(f"{config.run_name}.csv", index=False)
    log.info(
        f"\nMRE Error Mean: [Cp], {sum(test_cp_mre_list)/len(test_cp_mre_list)*100:.2f}%, [Cf], {sum(test_cf_mre_list)/len(test_cf_mre_list)*100:.2f}%, [Cd], {sum(test_loss_cd)/len(test_loss_cd)*100:.2f}%, [Cl], {sum(test_loss_cl)/len(test_loss_cl)*100} \tRelative L2 Error Mean : [P], {sum(test_loss_p)/len(test_loss_p):.4f}, [WSS], {sum(test_loss_wss)/len(test_loss_wss):.4f}, [VEL], {sum(test_loss_vel)/len(test_loss_vel):.4f}"
    )

    if config.mode == "train":
        model.train()
        return [
            test_l2_loss_list,
            test_mse_cd_loss_list,
            test_cp_mre_list,
            test_cf_mre_list,
        ]


def train(config, model, train_data, test_data, device):
    """
    使用PaddlePaddle框架训练模型

    Args:
        config (dict): 配置信息，包含学习率(lr)和训练轮数(num_epochs)等
        model (paddle.nn.Layer): 待训练的模型
        train_data (Iterable): 训练数据集
        test_data (Iterable): 测试数据集
        device (str): 计算设备，如'gpu'或'cpu'

    Returns:
        None
    """
    # 创建优化器
    optimizer = paddle.optimizer.AdamW(
        parameters=model.parameters(), learning_rate=config.lr, weight_decay=1e-6
    )

    # 启动数据并行
    if config.enable_ddp:
        # 实例化分布式策略
        strategy = fleet.DistributedStrategy()
        # 初始化分布式环境，设置is_collective为True表示使用集合通信方式
        fleet.init(is_collective=True, strategy=strategy)
        # 分布式模型封装
        model = fleet.distributed_model(model)
        # 分布式优化器
        optimizer = fleet.distributed_optimizer(optimizer)

    # 断点续训
    if config.checkpoint is not None:
        log.info(f"loading checkpoint from: {config.checkpoint}")
        load_checkpoint(config, model)
    if config.lr_schedular is not None:
        # 学习率调度器
        scheduler = paddle.optimizer.lr.CosineAnnealingDecay(
            learning_rate=optimizer.get_lr(), T_max=config.num_epochs
        )
        # 设置学习率调度器
        optimizer.set_lr_scheduler(scheduler)
    # 损失函数
    loss_fn = LpLoss(size_average=True)
    loss_cd_fn = paddle.nn.MSELoss()
    train_loss_list_p, train_loss_list_cd, train_cp_mre_list = [], [], []

    for ep in range(config.num_epochs):
        # 记录训练开始时间
        t1 = time.time()
        # 训练循环
        for n_iter, data in enumerate(train_data):
            # 模型前向传播
            output = model(data)
            (
                l2_loss,
                mse_cd_loss,
                loss_p,
                loss_wss,
                loss_vel,
                c_p_mre,
                c_f_mre,
                c_d_mre,
                c_l_mre,
            ) = car_loss(config, output, data, loss_fn, loss_cd_fn)
            if config.cd_finetune is True:
                train_loss = l2_loss + config.cd_loss_weight * mse_cd_loss
            else:
                train_loss = l2_loss
            train_cp_mre_list.append(c_p_mre)
            train_loss_list_p.append(train_loss.item())
            train_loss_list_cd.append(mse_cd_loss.item())
            # 清除梯度
            optimizer.clear_grad()
            # 反向传播
            train_loss.backward()
            # 更新模型参数
            optimizer.step()
        # 更新学习率
        if config.lr_schedular is not None:
            scheduler.step()
        # 测试循环
        (
            test_l2_loss_list,
            test_mse_cd_loss_list,
            test_cp_mre_list,
            test_cf_mre_list,
        ) = test(config, model, test_data, device)

        # 记录训练结束时间
        t2 = time.time()
        # 打印训练信息
        log_and_tensorboard(
            config,
            ep,
            (t2 - t1),
            optimizer.get_lr(),
            train_loss_list_p,
            train_loss_list_cd,
            train_cp_mre_list,
            test_l2_loss_list,
            test_mse_cd_loss_list,
            test_cp_mre_list,
            test_cf_mre_list,
        )

        # Save the weights
        if (ep + 1) % 50 == 0:
            paddle.save(
                model.state_dict(), f"{config.output_dir}/{config.model}_{ep}.pdparams"
            )
    # 训练结束保存模型参数
    paddle.save(model.state_dict(), f"{config.output_dir}/checkpoint_latest.pdparams")


@hydra.main(version_base=None, config_path="./configs", config_name="transolver.yaml")
def main(config):
    """
    主函数，用于训练和测试模型

    Args:
        config (dict): 包含模型配置信息的字典

    Returns:
        None
    """
    global tensorboard
    tensorboard = tensorboardX.SummaryWriter(
        os.path.join(config.output_dir, "tensorboard")
    )
    log.info(f"Working directory : {os.getcwd()}")
    log.info(
        f"Output directory  : {hydra.core.hydra_config.HydraConfig.get().runtime.output_dir}"
    )

    set_seed(config.seed)

    # 获取设备信息
    device = paddle.device.get_device()
    # 数据生成
    datamodule = instantiate_datamodule(
        config, config.n_train_num, 0, config.n_test_num
    )
    # 模型构建
    model = instantiate_network(config)

    # 模型训练
    test_loader = datamodule.test_dataloader(
        batch_size=config.batch_size, num_workers=0, enable_ddp=config.enable_ddp
    )
    if config.mode == "train":
        # 创建训练数据加载器
        train_loader = datamodule.train_dataloader(
            batch_size=config.batch_size, num_workers=0, enable_ddp=config.enable_ddp
        )
        train(config, model, train_loader, test_loader, device)
    # 模型测试
    elif config.mode == "test":
        # 创建测试数据加载器
        model.eval()
        test(config, model, test_loader, device)


if __name__ == "__main__":
    # python -m paddle.distributed.launch --gpus=2,4,5,6 main_v2.py --config-name=transolver.yaml mode=test enable_ddp=true data_module=fake +num_points=1000000 checkpoint=...
    # python  main_v2.py --config-name=transolver_starccm+.yaml
    # python  main_v2.py --config-name=UNet_DrivAer.yaml
    # python  main_v2.py --config-name=gino.yaml
    main()
