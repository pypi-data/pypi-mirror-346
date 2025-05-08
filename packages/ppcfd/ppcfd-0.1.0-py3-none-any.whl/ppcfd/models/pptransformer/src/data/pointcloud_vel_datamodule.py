import os
import time
from pathlib import Path

import numpy as np
import paddle
import vtk
from vtk.util.numpy_support import numpy_to_vtk
from vtk.util.numpy_support import vtk_to_numpy

from src.data.base_datamodule import BaseDataModule
from src.data.pointcloud_datamodule import load_mean_std
from src.data.starccm_datamodule import get_centroids
from src.data.starccm_datamodule import get_nodes


def load_velocity(polydata):
    point_data_keys = [
        polydata.GetCellData().GetArrayName(i)
        for i in range(polydata.GetCellData().GetNumberOfArrays())
    ]
    if "UMeanTrim" in point_data_keys:
        vel = vtk_to_numpy(polydata.GetCellData().GetArray("UMeanTrim")).astype(
            np.float32
        )
        return vel
    else:
        print("point_data_keys in polydata", point_data_keys)
        raise NotImplementedError("No velocity found in the point cloud file.")


class PointCloudDataset(paddle.io.Dataset):
    def __init__(self, root_dir, train=True, translate=True, test=False, num=1):
        """
        Args:
            root_dir (string): Directory with all the point cloud files.
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        self.root_dir = root_dir
        self.file_list = [f for f in os.listdir(root_dir) if (f.endswith(".vtp"))][:num]
        if len(self.file_list) == 0:
            raise RuntimeError(f"No files found in provided {root_dir} directory.")
        self.train = train
        self.translate = translate
        self.test = test

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        file_name = self.file_list[idx]
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(self.root_dir + file_name)
        reader.Update()
        polydata = reader.GetOutput()
        points = get_centroids(polydata)
        vel = load_velocity(polydata)[:, 0]
        points_min = np.min(points, axis=0, keepdims=True)
        points_max = np.max(points, axis=0, keepdims=True)
        mean_std_dict = load_mean_std(self.root_dir + "/../mean_std.paddledict")
        if self.train:
            sample_rate = 0.5
        else:
            sample_rate = 0.4

        if self.test:
            sampled_indices = np.arange(points.shape[0])
        else:
            sampled_indices = np.random.choice(
                np.arange(points.shape[0]),
                int(len(points) * sample_rate),
                replace=False,
            )

        sampled_points = points[sampled_indices].astype(np.float32)
        local_sampled_points = (sampled_points - points_min) / (
            points_max - points_min
        ).astype(np.float32)
        if self.translate and self.train:
            translation_vector = np.random.rand(3) * 0.01 - 0.005  # 随机平移向量
            sampled_points += translation_vector

        Normal = True
        if Normal:
            sampled_points = (
                sampled_points - mean_std_dict["centroid_mean"]
            ) / mean_std_dict["centroid_std"]

        sample = {
            "centroids": sampled_points.astype(np.float32),
            "local_centroid": local_sampled_points.astype(np.float32),
            "vel": vel[sampled_indices].astype(np.float32),
            "file_name": file_name.split(".")[0],
            "file_path": self.root_dir + file_name,
            "v_mean": mean_std_dict["vel_std"],
            "v_std": mean_std_dict["vel_mean"],
        }
        return sample


class PointCloud_Vel_DataModule(BaseDataModule):
    def __init__(self, train_data_dir, test_data_dir, n_train_num, n_test_num):
        BaseDataModule.__init__(self)
        self.train_data_dir = Path(train_data_dir)
        self.test_data_dir = Path(test_data_dir)
        if n_train_num != 0:
            self.train_data = PointCloudDataset(
                train_data_dir, train=True, test=False, num=n_train_num
            )
        self.test_data = PointCloudDataset(
            test_data_dir, train=False, test=True, num=n_test_num
        )

    def decode(self, data, idx: int) -> paddle.Tensor:
        return self.decoder[idx](data.T)

    def save_vtk(self, file_path, var, var_name, vtk_name):
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(file_path)
        reader.Update()
        polydata = reader.GetOutput()
        np_array = var.numpy()[0]
        vtk_array = numpy_to_vtk(np_array)
        vtk_array.SetName(var_name)  # 设置数据的名称
        polydata.GetCellData().AddArray(vtk_array)
        appendFilter = vtk.vtkAppendFilter()
        appendFilter.AddInputData(polydata)
        appendFilter.Update()
        writer = vtk.vtkUnstructuredGridWriter()
        writer.SetFileName(vtk_name)  # 设置输出文件的名称
        writer.SetInputData(appendFilter.GetOutput())
        writer.Write()
