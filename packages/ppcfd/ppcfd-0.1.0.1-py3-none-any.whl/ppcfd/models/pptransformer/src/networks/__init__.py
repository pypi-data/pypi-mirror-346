import operator
from functools import reduce

from .ConvUNet2 import UNet3DWithSamplePoints

try:
    import open3d

    # 如果 open3d 成功导入，则继续导入其他模块
    from .GNOFNOGNO import GNOFNOGNO
    from .GNOFNOGNO import GNOFNOGNOAhmed
except ImportError:
    print("open3d 库未安装，因此不会导入相关模块。")
from .KAN import KAN
from .Transolver import Transolver


def count_params(model):
    c = 0
    for p in list(model.parameters()):
        c += reduce(operator.mul, list(p.shape + (2,) if p.is_complex() else p.shape))
    return c


def instantiate_network(config):
    if False:
        pass
    elif config.model == "GNOFNOGNO":
        print("using GNOFNOGNO")
        model = GNOFNOGNO(
            radius_in=config.radius_in,
            radius_out=config.radius_out,
            embed_dim=config.embed_dim,
            hidden_channels=config.hidden_channels,
            in_channels=config.in_channels,
            out_channels=config.out_channels,
            fno_modes=config.fno_modes,
            fno_hidden_channels=config.fno_hidden_channels,
            fno_out_channels=config.fno_hidden_channels,
            fno_domain_padding=0.125,
            fno_norm="group_norm",
            fno_factorization="tucker",
            fno_rank=0.4,
            weighted_kernel=config.weighted_kernel,
        )
    elif config.model == "GNOFNOGNOAhmed":
        print("using GNOFNOGNOAhmed")
        model = GNOFNOGNOAhmed(
            radius_in=config.radius_in,
            radius_out=config.radius_out,
            embed_dim=config.embed_dim,
            hidden_channels=config.hidden_channels,
            in_channels=config.in_channels,
            out_channels=config.out_channels,
            fno_modes=config.fno_modes,
            fno_hidden_channels=config.fno_hidden_channels,
            fno_out_channels=config.fno_hidden_channels,
            fno_domain_padding=0.125,
            fno_norm="ada_in",
            fno_factorization="tucker",
            fno_rank=0.4,
            linear_kernel=True,
            weighted_kernel=config.weighted_kernel,
            subsample_train=config.subsample_train,
            subsample_eval=config.subsample_eval,
            max_in_points=config.max_in_points,
        )
    elif config.model == "UNet":
        print("using UNet")
        model = UNet3DWithSamplePoints(
            in_channels=config.in_channels,  # xyz + sdf
            out_channels=config.out_channels[0],
            hidden_channels=config.hidden_channels,
            num_levels=config.num_levels,
            use_position_input=config.use_position_input,
        )
    elif config.model == "Transolver":
        print("using Transolver")
        model = Transolver(
            space_dim=config.space_dim,
            n_layers=config.n_layers,
            n_hidden=config.n_hidden,
            dropout=config.dropout,
            n_head=config.n_head,
            act=config.act,
            mlp_ratio=config.mlp_ratio,
            fun_dim=config.fun_dim,
            out_dim=sum(config.out_channels),
            slice_num=config.slice_num,
            ref=config.ref,
            n_iter=config.n_iter,
            unified_pos=config.unified_pos,
        )
    elif config.model == "KAN":
        print("using KAN")
        model = KAN(layers_hidden=[3, 5, 5, 1], dim_latent=64)
    else:
        raise ValueError("Network not supported")

    print("The model size is ", count_params(model))
    return model
