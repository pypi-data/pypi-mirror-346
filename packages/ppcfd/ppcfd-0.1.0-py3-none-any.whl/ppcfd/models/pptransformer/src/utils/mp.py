import numpy as np
import paddle
import paddle.distributed as dist


def init_dist_env(config):
    if config.enable_mp:
        dim_names = ["mp"]
        mesh = dist.ProcessMesh(
            np.arange(0, paddle.distributed.get_world_size()), dim_names=dim_names
        )
    elif config.enable_pp:
        dim_names = ["pp"]
        mesh = dist.ProcessMesh(
            np.arange(0, paddle.distributed.get_world_size()), dim_names=dim_names
        )
        mesh = dist.ProcessMesh(
            [np.arange(0, paddle.distributed.get_world_size())], dim_names=["x", "pp"]
        )
    else:
        NotImplementedError("No distributed training enabled")

    assert paddle.distributed.get_world_size() > 1
    dist.auto_parallel.set_mesh(mesh)


def get_mesh():
    return dist.auto_parallel.get_mesh()


def shard_data_dict(data_dict: dict, shard_dim: int, ignore_keys: list = []):
    meshes = get_mesh()
    placements = [dist.Shard(shard_dim)]
    for key, value in data_dict.items():
        if isinstance(value, paddle.Tensor):
            if key in ignore_keys:
                continue
            data_dict[key] = dist.shard_tensor(value, meshes, placements)
    return data_dict


def replicate_data_dict(
    data_dict: dict,
    shard_dim: int = 1,
    ignore_keys: list = [
        "file_name",
        "p_mean",
        "p_std",
        "wss_mean",
        "wss_std",
        "reference_area",
    ],
):
    meshes = get_mesh()
    placements = [dist.Replicate()]
    new_data_dict = {}
    for key, value in data_dict.items():
        if isinstance(value, paddle.Tensor):
            if key in ignore_keys:
                new_data_dict[key] = data_dict[key]
            else:
                new_data_dict[key] = dist.reshard(value, meshes, placements)
        else:
            new_data_dict[key] = data_dict[key]

    return new_data_dict


def parallelize(model, optimizer, config):
    if model is None:
        raise NotImplementedError("Model is None")

    if config.enable_mp:
        parallel_config = {
            "mp_config": {"parallelize_plan": {}},
        }
        for name, layer in model.named_sublayers():
            layer_type = str(type(layer))
            if "Linear" in layer_type and "mlp2" not in name:
                parallel_config["mp_config"]["parallelize_plan"][
                    name
                ] = dist.ColWiseParallel()
    elif config.enable_pp:
        parallel_config = {
            # TODO: fix for other model
            "pp_config": {
                "split_spec": {
                    "preprocess.linear_post": dist.SplitPoint.END,
                    "blocks.0.pp_layer": dist.SplitPoint.END,
                    "blocks.1.pp_layer": dist.SplitPoint.END,
                },
            },
        }

    if model is not None or optimizer is not None:
        model, optimizer = dist.parallelize(
            model=model, optimizer=optimizer, config=parallel_config
        )
        for name, layer in model.named_sublayers():
            if hasattr(layer, "weight"):
                print(layer.weight.process_mesh.process_ids, name)
        return model, optimizer
