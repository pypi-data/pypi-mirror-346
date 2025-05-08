try:
    from .cfd_datamodule import AhmedBodyDataModule
    from .cfd_datamodule import CFDDataModule
    from .cfd_datamodule import CFDSDFDataModule
    from .datamodule_lazy import DrivAerDataModule
except ImportError:
    print("open3d 库未安装，因此不会导入相关模块。")

from .fake_datamodule import FakeDataModule
from .pde_cylinder_datamodule import PDE_Cylinder_DataModule
from .pointcloud_datamodule import PointCloudDataModule
from .pointcloud_vel_datamodule import PointCloud_Vel_DataModule
from .starccm_datamodule import StarCCMDataModule


def instantiate_datamodule(config, n_train_num=None, n_val_num=None, n_test_num=None):
    if config.data_module == "CFDDataModule":
        return CFDDataModule(
            config.data_path,
        )
    elif config.data_module == "CFDSDFDataModule":
        assert config.sdf_spatial_resolution is not None
        return CFDSDFDataModule(
            config.data_path,
            config.n_train_num,
            config.n_test_num,
            spatial_resolution=config.sdf_spatial_resolution,
            test_data_dir=config.test_data_dir,
        )
    elif config.data_module == "AhmedBodyDataModule":
        assert config.sdf_spatial_resolution is not None
        return AhmedBodyDataModule(
            config.data_path,
            config.test_data_dir,
            config.n_train,
            config.n_test,
            spatial_resolution=config.sdf_spatial_resolution,
        )
    elif config.data_module == "drivaer":
        assert config.sdf_spatial_resolution is not None
        return DrivAerDataModule(
            config.data_path,
            out_keys=config.out_keys,
            out_channels=config.out_channels,
            n_train=n_train_num if n_train_num is not None else config.n_train_num,
            n_val=n_val_num if n_val_num is not None else config.n_val_num,
            n_test=n_test_num if n_test_num is not None else config.n_test_num,
            spatial_resolution=config.sdf_spatial_resolution,
            lazy_loading=config.lazy_loading,
            only_save_sdf=config.only_save_sdf,
            subsample_train=config.subsample_train,
        )
    elif config.data_module == "starccm":
        return StarCCMDataModule(
            train_data_dir=config.data_path + "/train/",
            test_data_dir=config.data_path + "/test/",
            n_train_num=config.n_train_num,
            n_test_num=config.n_test_num,
            train_sample_number=config.train_sample_number,
        )
    elif config.data_module == "pointcloud":
        return PointCloudDataModule(
            train_data_dir=config.data_path + "/train/",
            test_data_dir=config.data_path + "/test/",
            n_train_num=config.n_train_num,
            n_test_num=config.n_test_num,
        )
    elif config.data_module == "pointcloud_vel":
        return PointCloud_Vel_DataModule(
            train_data_dir=config.data_path + "/train/",
            test_data_dir=config.data_path + "/test/",
            n_train_num=config.n_train_num,
            n_test_num=config.n_test_num,
        )
    elif config.data_module == "pde_cylinder":
        return PDE_Cylinder_DataModule(
            train_data_dir=config.data_path,
            test_data_dir=config.data_path + "/test/",
            n_train=config.n_train_num,
            n_test=config.n_test_num,
        )
    elif config.data_module == "fake":
        return FakeDataModule(
            num_points=config.num_points,
        )
    else:
        raise NotImplementedError(f"Unknown datamodule: {config.data_module}")
