import logging
import os

# paddle.device.set_device("cpu")
from pathlib import Path
from timeit import default_timer

import hydra
import numpy as np
import paddle
import vtk
from omegaconf import DictConfig
from paddle.distributed import fleet

from src.data import instantiate_datamodule
from src.data.starccm_datamodule import read_case
from src.data.starccm_datamodule import write
from src.networks import instantiate_network
from src.utils.average_meter import AverageMeterDict

strategy = fleet.DistributedStrategy()
fleet.init(is_collective=True, strategy=strategy)


def set_seed(seed: int = 0):
    paddle.seed(seed)
    np.random.seed(seed)


class LpLoss(object):
    def __init__(self, d=2, p=2, size_average=True, reduction=True):
        super(LpLoss, self).__init__()

        # Dimension and Lp-norm type are postive
        assert d > 0 and p > 0

        self.d = d
        self.p = p
        self.reduction = reduction
        self.size_average = size_average

    def abs(self, x, y):
        num_examples = x.size()[0]

        # Assume uniform mesh
        h = 1.0 / (x.size()[1] - 1.0)

        all_norms = (h ** (self.d / self.p)) * paddle.norm(
            x.reshape((num_examples, -1)) - y.reshape((num_examples, -1)), self.p, 1
        )

        if self.reduction:
            if self.size_average:
                return paddle.mean(all_norms)
            else:
                return paddle.sum(all_norms)

        return all_norms

    def rel(self, x, y):
        num_examples = x.shape[0]

        diff_norms = paddle.norm(
            x.reshape([num_examples, -1]) - y.reshape([num_examples, -1]), self.p, 1
        )
        y_norms = paddle.norm(y.reshape([num_examples, -1]), self.p, 1)

        if self.reduction:
            if self.size_average:
                return paddle.mean(diff_norms / y_norms)
            else:
                return paddle.sum(diff_norms / y_norms)

        return diff_norms / y_norms

    def __call__(self, x, y):
        return self.rel(x, y)


def train(cfg: DictConfig, with_val=False):
    # logging setting
    logging.basicConfig(
        filename=os.path.join(cfg.output_dir, f"{cfg.mode}.log"),
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )

    # Initialize the device
    # device = paddle.CUDAPlace(cfg.device)

    # Initialize the model
    model = instantiate_network(cfg)
    # Initialize the optimizer
    optimizer = paddle.optimizer.AdamW(
        parameters=model.parameters(), learning_rate=cfg.lr, weight_decay=1e-6
    )
    if cfg.enable_ddp:
        model = fleet.distributed_model(model)
        optimizer = fleet.distributed_optimizer(optimizer)

    scheduler = paddle.optimizer.lr.CosineAnnealingDecay(
        learning_rate=optimizer.get_lr(), T_max=cfg.num_epochs
    )
    optimizer.set_lr_scheduler(scheduler)

    resume_ep = cfg.resume_ep
    if cfg.checkpoint:
        # load param
        param_dict = paddle.load(f"{cfg.checkpoint}.pdparams")
        if "model_state_dict" in param_dict:
            model.set_state_dict(param_dict["model_state_dict"])
        else:
            model.set_state_dict(param_dict)
        # model.to(device)

        # load optimizer
        if os.path.exists(f"{cfg.checkpoint}.pdopt"):
            optim_dict = paddle.load(f"{cfg.checkpoint}.pdopt")
            optimizer.set_state_dict(optim_dict)
            resume_ep = optim_dict["LR_Scheduler"]["last_epoch"]
        else:
            for ep in range(resume_ep):
                scheduler.step()
                continue
        logging.info(f"lr of {resume_ep} is {optimizer.get_lr()}")
        # TODO: load GradScaler for AMP
    assert (
        cfg.num_epochs > resume_ep
    ), f"training epochs {cfg.num_epochs} should bigger than resume epoch, which is {resume_ep} now."

    # TODO: amp not supported now
    # scaler = paddle.amp.GradScaler(init_loss_scaling=1024)

    # Initialize the dataloaders
    n_val_num = cfg.n_val_num if with_val else 0
    t1 = default_timer()
    datamodule = instantiate_datamodule(cfg, cfg.n_train_num, n_val_num, 0)
    t2 = default_timer()
    logging.info(f"Loading data took {t2 - t1:.2f} seconds.")

    train_loader = datamodule.train_dataloader(
        batch_size=cfg.batch_size, num_workers=0, enable_ddp=cfg.enable_ddp
    )

    # evaluate while training
    if with_val:
        val_loader = datamodule.val_dataloader(
            batch_size=cfg.batch_size, num_workers=0, enable_ddp=cfg.enable_ddp
        )

    # Initialize the loss function
    loss_fn = LpLoss(size_average=True)

    logging.info(f"Start training {cfg.model} ...")

    for ep in range(resume_ep, cfg.num_epochs):
        t1 = default_timer()
        train_l2_meter = AverageMeterDict()

        for data_dict in train_loader:
            # TODO: amp not supported now
            # with paddle.amp.auto_cast(
            #     custom_black_list={
            #         "repeat_interleave",
            #         "repeat_interleave_with_tensor_index",
            #     },
            #     level="O1",
            # ):
            pred, truth = model(data_dict)
            # loss
            loss = paddle.to_tensor(0.0).cuda()
            for i in range(len(cfg.out_keys)):
                key = cfg.out_keys[i]
                st, end = (
                    sum(cfg.out_channels[:i]),
                    sum(cfg.out_channels[:i]) + cfg.out_channels[i],
                )
                loss_key = loss_fn(pred[st:end], truth[st:end])
                train_l2_meter.update({key: loss_key})
                loss += loss_key

            # scaled = scaler.scale(loss)
            # scaled.backward()
            # scaler.step(optimizer)
            # scaler.update()

            loss.backward()
            optimizer.step()
            optimizer.clear_grad(set_to_zero=False)

        scheduler.step()
        t2 = default_timer()

        msg = f"Training epoch {ep} took {t2 - t1:.2f} seconds. L2_Loss: "
        train_dict = train_l2_meter.avg
        for k, v in train_dict.items():
            msg += f"{v.item():.4f}({k}), "
        logging.info(msg)

        def eval_in_train():
            model.eval()
            metric_p = 0
            metric_wss = 0
            with paddle.no_grad():
                for test_data_dict in val_loader:
                    t1 = default_timer()
                    pred, truth = model(test_data_dict)
                    if "pressure" in cfg.out_keys:
                        metric_p += loss_fn(pred[:1], truth[:1]).item()
                        if "wss" in cfg.out_keys:
                            metric_wss += loss_fn(pred[1:], truth[1:]).item()
                    else:
                        metric_wss += loss_fn(pred, truth).item()
                t2 = default_timer()
                metric_p /= n_val_num
                metric_wss /= n_val_num
            logging.info(
                f"Test took {t2 - t1:.2f} s. L2_Error: {metric_p:.4f}(p), {metric_wss:.4f}(wss)"
            )

        # Save the weights
        if (ep + 1) % cfg.save_freq == 0 or ep == cfg.num_epochs - 1 or (ep + 1) == 1:
            paddle.save(
                model.state_dict(), f"{cfg.output_dir}/{cfg.model}_{ep}.pdparams"
            )
            if optimizer:
                paddle.save(
                    optimizer.state_dict(), f"{cfg.output_dir}/{cfg.model}_{ep}.pdopt"
                )
            if with_val and (ep + 1) != 1:
                # eval
                eval_in_train()


@paddle.no_grad()
def evaluate(cfg: DictConfig):
    # logging setting
    logging.basicConfig(
        filename=os.path.join(cfg.output_dir, f"{cfg.mode}.log"),
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )

    # Initialize the device
    # device = paddle.CUDAPlace(cfg.device)

    # Initialize the model
    model = instantiate_network(cfg)

    # load checkpoint
    assert cfg.checkpoint is not None, "checkpoint must be given."
    checkpoint = paddle.load(f"{cfg.checkpoint}.pdparams")
    if "model_state_dict" in checkpoint:
        model.set_state_dict(checkpoint["model_state_dict"])
    else:
        model.set_state_dict(checkpoint)

    # Initialize the dataloaders
    t1 = default_timer()
    datamodule = instantiate_datamodule(cfg, 1, 0, cfg.n_test_num)
    t2 = default_timer()
    logging.info(f"Loading data took {t2 - t1:.2f} seconds.")
    test_loader = datamodule.test_dataloader(
        batch_size=cfg.batch_size, num_workers=0, enable_ddp=cfg.enable_ddp
    )

    # Initialize the loss function
    loss_fn = LpLoss(size_average=True)

    # eval
    logging.info(f"Start evaluting {cfg.model} ...")

    t1 = default_timer()

    eval_meter = AverageMeterDict()
    visualize_data_dicts = []

    def mre(pred, label):
        return paddle.abs(pred - label) / paddle.abs(label)

    for i, data_dict in enumerate(test_loader):
        out_dict = model.eval_dict(
            data_dict, loss_fn=loss_fn, decode_fn=datamodule.decode
        )

        print_dict = {}
        for k, v in out_dict.items():
            if k.split("_")[0] not in ["pred", "truth"]:
                print_dict[k] = v
        eval_meter.update(print_dict)

        msg = f"Eval sample {i}... L2_Error: "
        for k in cfg.out_keys:
            k1 = k + " l2"
            msg += f"{out_dict[k1].item():.4f}({k1}), "
            # if decode
            k2 = k + " l2 decoded"
            msg += f"{out_dict[k2].item():.4f}({k2}), "

        msg += "MRE: "
        for k in cfg.out_keys:
            mre_key = mre(out_dict[f"drag_pred_{k}"], out_dict[f"drag_truth_{k}"])
            eval_meter.update({f"{k} mre": mre_key})
            msg += f"{mre_key.item():.4f}({k}), "

        # if decode
        if len(cfg.out_keys) >= 2:
            mre_cd = mre(out_dict["drag_pred"], out_dict["drag_truth"])
            eval_meter.update({"cd": mre_cd})
            msg += f"CD: {mre_cd.item():.4f}"
        logging.info(msg)

        if cfg.data_module == "starccm":
            os.makedirs("output_vtk", exist_ok=True)
            file_path = Path(data_dict["file_path"][0])
            file_name = data_dict["file_name"][0]
            body = Path("body_vtk.case")
            whel = Path("wheel_vtk.case")
            _, polydata_body = read_case(file_path / body)
            _, polydata_whel = read_case(file_path / whel)
            appendFilter = vtk.vtkAppendFilter()
            appendFilter.AddInputData(polydata_body)
            appendFilter.AddInputData(polydata_whel)
            appendFilter.Update()
            polydata = appendFilter.GetOutput()
            write(
                polydata,
                out_dict["pred_pressure"],
                "pred_pressure",
                f"./output_vtk/predit_{file_name}_p.vtk",
            )
            write(
                polydata,
                out_dict["pred_wss"],
                "pred_wss",
                f"./output_vtk/predit_{file_name}_wss.vtk",
            )

    # Merge all dictionaries
    merged_image_dict = {}
    if hasattr(model, "image_dict"):
        for i, data_dict in enumerate(visualize_data_dicts):
            image_dict = model.image_dict(data_dict)
            for k, v in image_dict.items():
                merged_image_dict[f"{k}_{i}"] = v

    t2 = default_timer()

    msg = f"Testing took {t2 - t1:.2f} seconds. Eval values: "
    eval_dict = eval_meter.avg
    for k, v in eval_dict.items():
        msg += f"{v.item():.4f}({k}), "
    logging.info(msg)


def export(cfg: DictConfig):
    from paddle import jit
    from paddle import nn
    from paddle.static import InputSpec

    # logging setting
    logging.basicConfig(
        filename=os.path.join(cfg.output_dir, f"{cfg.mode}.log"),
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )

    # Initialize the model
    model = instantiate_network(cfg)

    # load checkpoint
    assert cfg.checkpoint is not None, "checkpoint must be given."
    checkpoint = paddle.load(f"{cfg.checkpoint}.pdparams")
    if "model_state_dict" in checkpoint:
        model.set_state_dict(checkpoint["model_state_dict"])
    else:
        model.set_state_dict(checkpoint)

    class Wrapped_Model(nn.Layer):
        def __init__(self, model):
            super().__init__()
            self.model = model

        def forward(self, data_dict):
            pred = self.model.export(data_dict)
            return pred

    wrapped_model = Wrapped_Model(model)

    info_keys = [
        "length",
        "width",
        "height",
        "clearance",
        "slant",
        "radius",
        "velocity",
        "re",
        "reference_area",
        "compute_normal",
    ]

    input_spec = [
        {
            "df": InputSpec([1, 64, 64, 64], "float32"),
            "sdf_query_points": InputSpec([1, 3, 64, 64, 64], "float32"),
            "centroids": InputSpec([1, None, 3], "float32"),
            "closest_points": InputSpec([1, 3, 64, 64, 64], "float32"),
            "areas": InputSpec([1, None], "float32"),
            "vertices": InputSpec([1, 1], "float32"),
            "c_p": InputSpec([1, None], "float32"),
            "c_wss": InputSpec([1, 3, None], "float32"),
            "pressure": InputSpec([1, None], "float32"),
            "wss": InputSpec([1, None, 3], "float32"),
            "info": [
                {
                    key: InputSpec([], "float32")
                    if key != "compute_normal"
                    else InputSpec([], "bool")
                    for key in info_keys
                }
            ],
        }
    ]

    jit.enable_to_static(True)
    # convert model to static graph model
    static_model = jit.to_static(wrapped_model, input_spec=input_spec, full_graph=True)
    export_path = os.path.join(cfg.output_dir, "gino")

    # save static graph model to disk
    try:
        jit.save(static_model, export_path, skip_prune_program=True)
    except Exception as e:
        raise e
    jit.enable_to_static(False)


def inference(cfg: DictConfig):
    from typing import List

    import paddle.inference as paddle_infer

    from src.paddle_custom_operator.ops import CustomOps

    # logging setting
    logging.basicConfig(
        filename=os.path.join(cfg.output_dir, f"{cfg.mode}.log"),
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )

    cus_ops = CustomOps()
    input_keys = [
        "df",
        "sdf_query_points",
        "pressure",
        "vertices",
        "c_wss",
        "closest_points",
        "wss",
        "c_p",
        "areas",
        "centroids",
    ]
    info_keys = [
        "length",
        "width",
        "height",
        "clearance",
        "slant",
        "radius",
        "velocity",
        "re",
        "reference_area",
        "compute_normal",
    ]

    # setting config
    config = paddle_infer.Config(
        f"{cfg.infer_path}.pdmodel", f"{cfg.infer_path}.pdiparams"
    )
    config.enable_use_gpu(1024, 0)
    config.enable_memory_optim()
    config.switch_use_feed_fetch_ops(False)
    config.switch_ir_optim(True)
    predictor = paddle_infer.create_predictor(config)

    # Initialize the dataloaders
    datamodule = instantiate_datamodule(cfg, 1, 0, cfg.n_test_num)
    test_loader = datamodule.test_dataloader(
        batch_size=cfg.batch_size,
        num_workers=0,
        enable_ddp=False,
    )

    visualize_data_dicts = []
    for i, data_dict in enumerate(test_loader):
        # prepare input handle(s)
        input_handles = {}
        for name in input_keys + info_keys:
            input_handles.update({name: predictor.get_input_handle(name)})

        # prepare output handle(s)
        output_handles = {
            "pred": predictor.get_output_handle(predictor.get_output_names()[0])
        }

        # prepate data
        for name in input_keys:
            if name == "vertices":
                input_handles[name].copy_from_cpu(np.array([0.0], dtype="float32"))
            else:
                input_handles[name].copy_from_cpu(
                    np.array(data_dict[name], dtype="float32")
                )
        for name in info_keys:
            input_handles[name].copy_from_cpu(
                np.array(data_dict["info"][0][name], dtype="float32")
            )

        predictor.run()
        pred = paddle.to_tensor(output_handles["pred"].copy_to_cpu())

        out_dict = {}

        def decode(key, st, end, i):
            truth_key = data_dict[key][0]
            if len(truth_key.shape) == 1:
                truth_key = truth_key.reshape([-1, 1])
            truth_key = truth_key[:, : (end - st)].transpose(perm=[1, 0])
            pred_key = pred[st:end, :]
            if datamodule.decode is not None:
                pred_decode = datamodule.decode(pred_key, i)
                truth_decode = datamodule.decode(truth_key, i)
                out_dict.update(
                    {f"pred_{key}": pred_decode, f"truth_{key}": truth_decode}
                )

        # change 'st' 'end' accroding to 'out_keys' of config!!!
        if "pressure" in data_dict:
            decode("pressure", st=0, end=1, i=0)
        if "wss" in data_dict:
            decode("wss", st=1, end=4, i=1)

        # save vtk
        if "mesh" in data_dict:
            mesh = data_dict["mesh"][0]
            mesh.cell_data = {}
            for k in cfg.out_keys:
                pred_key = out_dict[f"pred_{k}"].T.cpu().numpy()
                truth_key = out_dict[f"truth_{k}"].T.cpu().numpy()
                error_key = np.abs(pred_key - truth_key)
                mesh.cell_data.update(
                    {
                        f"pred_{k}": pred_key,
                        f"truth_{k}": truth_key,
                        f"error_{k}": error_key,
                    }
                )
                mesh.write(os.path.join(cfg.output_dir, f"test_{i}.vtk"))
            visualize_data_dicts.append(data_dict)


@hydra.main(version_base=None, config_path="./configs", config_name="gino.yaml")
def main(cfg: DictConfig):
    if cfg.seed is not None:
        set_seed(cfg.seed)
    if cfg.mode == "train":
        print("################## training #####################")
        train(cfg)
    elif cfg.mode == "valid":
        print("################## training with validation #####################")
        train(cfg, with_val=True)
    elif cfg.mode == "test":
        print("################## test #####################")
        evaluate(cfg)
    elif cfg.mode == "export":
        print("################## export #####################")
        export(cfg)
    elif cfg.mode == "infer":
        print("################## inference #####################")
        inference(cfg)
    else:
        raise ValueError(
            f"cfg.mode should in ['train', 'valid', 'test'], but got '{cfg.mode}'"
        )


if __name__ == "__main__":
    # python -m paddle.distributed.launch --gpus=5,6 gino.py
    main()
