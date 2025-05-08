import os
import sys
from pathlib import Path

import numpy as np
import paddle
import vtk
from vtk.util.numpy_support import numpy_to_vtk
from vtk.util.numpy_support import vtk_to_numpy

from src.data.base_datamodule import BaseDataModule
from src.neuralop.utils import UnitGaussianNormalizer

sys.path.append("./PaddleScience/")
sys.path.append("/home/aistudio/3rd_lib")

try:
    import open3d

    def load_sdf_queries(min_bounds, max_bounds):
        tx = np.linspace(min_bounds[0], max_bounds[0], 64)
        ty = np.linspace(min_bounds[1], max_bounds[1], 64)
        tz = np.linspace(min_bounds[2], max_bounds[2], 64)
        sdf_query_points = np.stack(
            np.meshgrid(tx, ty, tz, indexing="ij"), axis=-1
        ).astype(np.float32)
        return sdf_query_points

    def load_sdf(file_path, sdf_query_points):
        mesh = open3d.io.read_triangle_mesh(str(file_path))
        mesh = open3d.t.geometry.TriangleMesh.from_legacy(mesh)
        scene = open3d.t.geometry.RaycastingScene()
        _ = scene.add_triangles(mesh)
        sdf = scene.compute_distance(sdf_query_points).numpy()
        sdf = sdf[np.newaxis, :]
        return sdf

    def load_sdf_from_vtk(polydata_triangle, sdf_query_points):
        points = vtk_to_numpy(polydata_triangle.GetPoints().GetData()).astype(
            np.float32
        )
        triangles = vtk_to_numpy(polydata_triangle.GetPolys().GetData()).astype(
            np.float32
        )
        mesh = open3d.geometry.TriangleMesh()
        mesh.vertices = open3d.utility.Vector3dVector(points)
        mesh.triangles = open3d.utility.Vector3iVector(triangles.reshape(-1, 4)[:, 1:])
        mesh = open3d.t.geometry.TriangleMesh.from_legacy(mesh)
        scene = open3d.t.geometry.RaycastingScene()
        _ = scene.add_triangles(mesh)
        sdf = scene.compute_distance(sdf_query_points).numpy()
        sdf = sdf
        return sdf

except ImportError:
    print("open3d 库未安装，因此不会导入相关模块。")


def normalization(locations, min_bounds, max_bounds):
    locations = (locations - min_bounds) / (max_bounds - min_bounds)
    locations = 2 * locations - 1
    return locations


def load_bound(data_dir):
    print((data_dir / "mean_std.paddledict").as_posix())
    mean_std_dict = paddle.load((data_dir / "mean_std.paddledict").as_posix())
    p_mean = mean_std_dict["p_mean"]
    p_std = mean_std_dict["p_std"]
    wss_x_mean = mean_std_dict["wss_x_mean"]
    wss_x_std = mean_std_dict["wss_x_std"]
    return p_mean, p_std, wss_x_mean, wss_x_std


def normalizer(data_dir):
    p_norm = UnitGaussianNormalizer(
        paddle.zeros(5), eps=1e-06, reduce_dim=0, verbose=False
    )
    p_mean, p_std, wss_x_mean, wss_x_std = load_bound(data_dir)
    p_norm.mean, p_norm.std = p_mean, p_std
    wss_norm = UnitGaussianNormalizer(
        paddle.zeros(5), eps=1e-06, reduce_dim=0, verbose=False
    )
    wss_norm.mean, wss_norm.std = wss_x_mean, wss_x_std
    return [p_norm.decode, wss_norm.decode], [p_norm.encode, wss_norm.encode]


def location_normalization(locations, min_bounds, max_bounds):
    min_bounds = paddle.to_tensor(min_bounds)
    max_bounds = paddle.to_tensor(max_bounds)
    locations = (locations - min_bounds) / (max_bounds - min_bounds)
    locations = 2 * locations - 1
    return locations


def read_ply(file_path):
    reader = vtk.vtkPLYReader()
    reader.SetFileName(file_path)
    reader.Update()
    polydata = reader.GetOutput()
    return reader, polydata


def read_stl(file_path):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(file_path)
    reader.Update()
    polydata = reader.GetOutput()
    return reader, polydata


def read_obj(file_path):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(file_path)
    reader.Update()
    polydata = reader.GetOutput()
    return reader, polydata


def read_vtk(file_path):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(file_path)
    reader.Update()
    polydata = reader.GetOutput()
    # point_data_keys = [
    #     polydata.GetPointData().GetArrayName(i)
    #     for i in range(polydata.GetPointData().GetNumberOfArrays())
    # ]
    # cell_data_keys = [
    #     polydata.GetCellData().GetArrayName(i)
    #     for i in range(polydata.GetCellData().GetNumberOfArrays())
    # ]
    # print("Point Data Keys:", point_data_keys)
    # print("Cell Data Keys:", cell_data_keys)
    return reader, polydata


def get_normals(polydata):
    normals_filter = vtk.vtkPolyDataNormals()
    normals_filter.SetInputData(polydata)
    normals_filter.ComputeCellNormalsOn()
    normals_filter.ConsistencyOn()
    normals_filter.FlipNormalsOn()
    normals_filter.AutoOrientNormalsOn()
    normals_filter.Update()
    numpy_cell_normals = vtk_to_numpy(
        normals_filter.GetOutput().GetCellData().GetNormals()
    ).astype(np.float32)
    return numpy_cell_normals


def get_areas(polydata):
    cell_size_filter = vtk.vtkCellSizeFilter()
    cell_size_filter.SetInputData(polydata)
    cell_size_filter.ComputeAreaOn()
    cell_size_filter.Update()
    numpy_cell_areas = vtk_to_numpy(
        cell_size_filter.GetOutput().GetCellData().GetArray("Area")
    ).astype(np.float32)
    return numpy_cell_areas


def get_centroids(polydata):
    cell_centers = vtk.vtkCellCenters()
    cell_centers.SetInputData(polydata)
    cell_centers.Update()
    numpy_cell_centers = vtk_to_numpy(
        cell_centers.GetOutput().GetPoints().GetData()
    ).astype(np.float32)
    return numpy_cell_centers


def get_nodes(polydata):
    points = vtk_to_numpy(polydata.GetPoints().GetData()).astype(np.float32)
    return points


def velocity(polydata):
    vel = vtk_to_numpy(polydata.GetPointData().GetArray("point_vectors")).astype(
        np.float32
    )
    return vel


def write(polydata, p, var_name, vtk_name):
    np_array = p.numpy()
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


def write_ply(polydata, filename):
    writer = vtk.vtkPLYWriter()
    writer.SetFileName(filename)  # 设置输出文件的名称
    writer.SetInputData(polydata)
    writer.Write()
    writer.SetInputData(polydata)
    writer.Write()


def normlalize_input(points, mean_std_dict_dir, sampled_indices=None):
    mean_std_dict = load_mean_std(mean_std_dict_dir)
    # points
    if sampled_indices is None:
        sampled_indices = np.arange(points.shape[0])
    points_min = np.min(points, axis=0, keepdims=True)
    points_max = np.max(points, axis=0, keepdims=True)
    sampled_points = points[sampled_indices]
    local_sampled_points = (sampled_points - points_min) / (points_max - points_min)
    # sampled_points = (sampled_points - mean_std_dict["centroid_mean"]) / mean_std_dict["centroid_std"]
    return {
        "centroids": paddle.to_tensor(sampled_points),
        "local_centroid": paddle.to_tensor(local_sampled_points),
        "p_mean": mean_std_dict["press_std"],
        "p_std": mean_std_dict["press_std"],
        "wss_mean": mean_std_dict["wss_mean"],
        "wss_std": mean_std_dict["wss_std"],
    }


class StarCCMDataset(paddle.io.Dataset):
    def __init__(self, file_list, test_mode=False, train_sample_number=70000):
        self.file_list = file_list
        self.len = len(file_list)
        self.test_mode = test_mode
        self.train_sample_number = train_sample_number

    def __getitem__(self, index):
        data_dir = self.file_list[index]
        data_dir = data_dir.with_suffix(".paddledict")
        data_dict = paddle.load(data_dir.as_posix())
        centroids = data_dict["centroids"]
        mean_std_dict = paddle.load(
            (data_dir.parent.parent / "mean_std.paddledict").as_posix()
        )
        data_dict.update(mean_std_dict)
        data_dict["local_centroid"] = (
            data_dict["centroids"] - paddle.min(centroids, axis=0, keepdim=True)
        ) / (
            paddle.max(centroids, axis=0, keepdim=True)
            - paddle.min(centroids, axis=0, keepdim=True)
        )
        n = data_dict["centroids"].shape[0]
        if self.test_mode == True:
            sampled_indices = np.arange(n)
        else:
            sampled_indices = np.random.choice(
                n, np.min([self.train_sample_number, n]), replace=False
            )
        data_dict["centroids"] = data_dict["centroids"][sampled_indices]
        data_dict["local_centroid"] = data_dict["local_centroid"][sampled_indices]
        data_dict["pressure"] = data_dict["pressure"][sampled_indices]
        data_dict["wss"] = data_dict["wss"][sampled_indices]
        data_dict["wss_mean"] = data_dict["wss_x_mean"]
        data_dict["wss_std"] = data_dict["wss_x_std"]
        data_dict["file_dir"] = data_dir.as_posix()
        data_dict["file_name"] = data_dir.name
        data_dict["areas"] = data_dict["areas"][sampled_indices]
        data_dict["normal"] = data_dict["normal"][sampled_indices]
        return data_dict

    def __len__(self):
        return self.len


class StarCCMDataModule(BaseDataModule):
    def __init__(
        self,
        train_data_dir,
        test_data_dir,
        n_train_num,
        n_test_num,
        train_sample_number,
    ):
        BaseDataModule.__init__(self)
        self.train_data_dir = Path(train_data_dir)
        self.test_data_dir = Path(test_data_dir)
        self.train_file_list = self.check_index_list(self.train_data_dir, n_train_num)
        self.test_file_list = self.check_index_list(self.test_data_dir, n_test_num)
        print("train_file_list number : ", len(self.train_file_list))
        print("test_file_list  number : ", len(self.test_file_list))
        self.train_data = StarCCMDataset(
            self.train_file_list, train_sample_number=train_sample_number
        )
        self.test_data = StarCCMDataset(self.test_file_list, test_mode=True)
        self.decoder, self.encoder = normalizer(self.train_data_dir.parent)

    def check_index_list(self, data_dir, n_data_num):
        file_list = [Path(f) for f in os.listdir(data_dir)][:n_data_num]
        new_file_list = []
        for f in file_list:
            f = data_dir / f
            new_file_list.append(f)
        return new_file_list

    def decode(self, data, idx: int) -> paddle.Tensor:
        return self.decoder[idx](data.T)
