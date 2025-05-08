# 加入mm与m的判断并自动转换
# @zhuhy根据上汽这边数据做出的修改版本，对应了viewer.py
# 新增计时功能，可以看每个文件的处理时间
import os
import re
import sys
import time
import json  
from pathlib import Path

import hydra
import numpy as np
import paddle
import pymeshlab
import streamlit as st
import vtk
from hydra import compose
from hydra import initialize
from hydra.core.global_hydra import GlobalHydra

sys.path.append(".")
from src.networks import instantiate_network
from src.utils.loss import LpLoss

sys.path.append("./src/script/starccm+/")

from main_v2 import calculate_coefficient
from main_v2 import denormalize
from main_v2 import load_checkpoint
from src.data.pointcloud_datamodule import normlalize_input as normlalize_input_points
from src.data.starccm_datamodule import get_areas
from src.data.starccm_datamodule import get_centroids
from src.data.starccm_datamodule import get_normals
from src.data.starccm_datamodule import normlalize_input as normlalize_input_star
from src.data.starccm_datamodule import write
from src.script.starccm_plus.pyfrontal import calculate_frontal_area


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

def convert_mm_to_m(polydata):
    """
    将几何体的单位从毫米 (mm) 转换为米 (m)，通过缩放几何体。
    """
    transform = vtk.vtkTransform()
    transform.Scale(0.001, 0.001, 0.001)  # 缩放因子：1 mm = 0.001 m
 
    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputData(polydata)
    transform_filter.SetTransform(transform)
    transform_filter.Update()
 
    return transform_filter.GetOutput()

def detect_and_convert_units(polydata):
    """
    检测几何体的单位，并在必要时从 mm 转换为 m。
    """
    if not polydata:
        raise ValueError("Input polydata is empty or invalid.")
    bounds = polydata.GetBounds()
    x_length = abs(bounds[1] - bounds[0])  # x方向的长度
    print(f"Detected x length: {x_length}")
 
    # 如果 x 长度大于 10，则假设单位为 mm，并转换为 m
    if x_length > 10:
        print("Detected unit as mm. Converting to meters...")
        polydata = convert_mm_to_m(polydata)
        # 重新计算边界框，因为几何体已被缩放
        bounds = polydata.GetBounds()
        print(f"Converted bounds: {bounds}")
 
    return polydata

def read_geometry(file_path, large_stl=False):
    if large_stl:
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(file_path.as_posix())
        ms.apply_filter(
            "meshing_decimation_quadric_edge_collapse",
            targetfacenum=100000,
            preservenormal=True,
        )
        # ms.apply_filter('meshing_decimation_clustering', threshold = pymeshlab.PercentageValue(0.182621))
        file_path = file_path.with_stem(file_path.stem + "_simplified")
        ms.save_current_mesh(file_path.as_posix())

    if file_path.suffix == ".ply":
        reader, polydata = read_ply(file_path)
    elif file_path.suffix == ".stl":
        reader, polydata = read_stl(file_path)
    elif file_path.suffix == ".obj":
        reader, polydata = read_obj(file_path)
    else:
        raise ValueError("Unsupported geometry format")
    polydata = detect_and_convert_units(polydata)  # 检测并转换单位
    return None, polydata

def get_bounds_info(polydata):
    bounds = polydata.GetBounds()
    return {
        "x_min": bounds[0],
        "x_max": bounds[1],
        "y_min": bounds[2],
        "y_max": bounds[3],
        "z_min": bounds[4],
        "z_max": bounds[5],
    }
 


def get_bounds_info(polydata):
    bounds = polydata.GetBounds()
    return {
        "x_min": bounds[0],
        "x_max": bounds[1],
        "y_min": bounds[2],
        "y_max": bounds[3],
        "z_min": bounds[4],
        "z_max": bounds[5],
    }
 

@hydra.main(
    version_base=None,
    config_path="../../src/script/test/",
    config_name="transolver.yaml",
)
def inference(config):
    start_time = time.time()
    output_dir = Path(config.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    input_filename = Path(config.input_filename)
    _, polydata = read_geometry(input_filename, config.large_stl)
    if config.data_module == "starccm":
        normlalize_input = normlalize_input_star
    elif config.data_module == "pointcloud":
        normlalize_input = normlalize_input_points
    else:
        raise NotImplementedError

    data = {}
    if config.mode == "test":
        data["centroids"] = np.load("./data_drivaer/test/centroid_0014.npy").astype(
            np.float32
        )
        data["areas"] = np.load("./data_drivaer/test/area_0014.npy").reshape([1, -1])
        data["normal"] = np.load("./data_drivaer/test/normal_0014.npy").reshape(
            [1, -1, 3]
        )
        data["pressure"] = np.load("./data_drivaer/test/press_0014.npy").reshape(
            [1, -1]
        )
        data["pressure"] = paddle.to_tensor(data["pressure"])
        data["wss"] = np.load("./data_drivaer/test/wallshearstress_0014.npy").reshape(
            [1, -1, 3]
        )
        data["wss"] = paddle.to_tensor(data["wss"])
        data["reference_area"] = [3]
    elif config.mode == "inference":
        data["centroids"] = get_centroids(polydata)
        data["areas"] = get_areas(polydata).reshape([1, -1])
        data["normal"] = get_normals(polydata).reshape([1, -1, 3])
        data["reference_area"] = [
            calculate_frontal_area(
                file_name=input_filename.as_posix(),
                vtk_data=polydata,
                proj_axis="X",
                debug=False,
            )[0]
        ]
        data["pressure"] = None
    else:
        raise ValueError("mode must be test or inference")

    mean_std_dict_dir = (Path(config.data_path) / "mean_std.paddledict").as_posix()
    data_input = normlalize_input(data["centroids"], mean_std_dict_dir)
    data = {**data, **data_input}

    def model_fn(config):
        model = instantiate_network(config)
        load_checkpoint(config, model)

        with paddle.no_grad():
            output = model(data)

        _, (
            p_true,
            p_pred,
            wss_true,
            wss_pred,
            wss_x_true,
            wss_x_pred,
            vel_true,
            vel_pred,
        ) = denormalize(config, data, output, config.mode)
        return p_true, p_pred, wss_x_true, wss_x_pred, wss_true, wss_pred, vel_true, vel_pred

    checkpoint_list = config.checkpoint
    config.checkpoint = checkpoint_list[0]
    config.out_channels = [1]
    config.out_keys = ["pressure"]
    p_true, p_pred, _, _, _, _, vel_true, vel_pred = model_fn(config)
    write(
        polydata,
        p_pred[0],
        f"pred_{config.out_keys[0]}",
        (output_dir / config.output_filename).as_posix(),
    )

    config.checkpoint = checkpoint_list[1]
    config.out_channels = [3]
    config.out_keys = ["wss"]
    _, _, wss_x_true, wss_x_pred, wss_true, wss_pred, vel_true, vel_pred = model_fn(config)
    write(
        polydata,
        wss_pred[0],
        f"pred_{config.out_keys[0]}",
        (output_dir / config.output_filename).as_posix(),
    )

    # case_data_dict = paddle.load('./temp_case_to_paddledict/train/test.case.paddledict')
    # p_pred = case_data_dict["pressure"].reshape([1, -1, 1])
    # wss_x_pred = case_data_dict["wss"][:,0]
    # wss_x_true = wss_x_pred

    data["coefficient"] = calculate_coefficient(
        data,
        p_pred,
        p_true,
        wss_x_pred,
        wss_x_true,
        config.mass_density,
        config.flow_speed,
    )

    print(
        "c_p_pred",
        data["coefficient"][0].item(),
        "c_f_pred",
        data["coefficient"][3].item(),
        "c_d_pred",
        data["coefficient"][6].item(),
    )

    if config.mode == "test":
        loss_fn = LpLoss(size_average=True)
        loss_p = loss_fn(p_true, p_pred).item()
        print("loss: ", loss_p)

    var = {
        "pressure":p_pred[0],
        "wss":wss_pred[0],
        "wss_x":wss_x_pred[0],
        "vel":vel_pred,
    }

    write(
        polydata,
        var[config.out_keys[0]],
        f"pred_{config.out_keys[0]}",
        (output_dir / config.output_filename).as_posix(),
    )

    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    print(f"Processing file {input_filename} took {elapsed_time:.2f} seconds.")

    # 定义数据
    data = {
        "vtk_dir": output_dir.as_posix(),  
        "coefficient": {  
            "c_p_pred": data["coefficient"][0].item(),  
            "c_f_pred": data["coefficient"][3].item(),  
            "c_d_pred": data["coefficient"][6].item()
        }  
    }  

    # 转换为JSON字符串  
    json_data = json.dumps(data, indent=4)  
    
    # 将JSON字符串写入文件
    txt_dir = Path("./output/predict_result.json")
    with open(txt_dir.as_posix(), "w") as f:  
        f.write(json_data)

inference()

# python src/web/predict.py --config-path=../../src/script/inference/ --config-name=transolver.yaml input_filename=/mnt/cfd/leiyao/workspace/DNNFluid-Car_web_viewer_fix/output/DrivAer_F_D_WM_WW_0001.stl output_filename=test_pred.vtk
# python src/web/predict.py --config-path=../../src/script/inference/ --config-name=transolver.yaml input_filename=./data_drivaer/test/mesh_rec_0001.ply output_filename=test_pred.vtk
# python src/web/predict.py --config-path=../../src/script/inference/ --config-name=transolver.yaml input_filename=./data_fake_starccm+/test.case.ply output_filename=test_pred.vtk flow_speed=33.33 mass_density=1.169 large_stl=True
