import json
import os
from pathlib import Path

import numpy as np
import paddle

from src.data.base_datamodule import BaseDataModule


def load_mean_std(input_file):
    """
    Load mean and standard deviations from a text file.
    Args:
    input_file (str): The path to the text file containing the saved
    mean and std values.

    Returns:
    dict: A dictionary with keys as the data categories and values as
    tuples of mean and std.
    """

    return paddle.load(input_file)


def normlalize_input(points, mean_std_dict_dir, sampled_indices=None, train=True):
    mean_std_dict = load_mean_std(mean_std_dict_dir)
    # points
    if sampled_indices is None:
        sampled_indices = np.arange(points.shape[0])
    points_min = np.min(points, axis=0, keepdims=True)
    points_max = np.max(points, axis=0, keepdims=True)
    sampled_points = points[sampled_indices]
    local_sampled_points = (sampled_points - points_min) / (points_max - points_min)
    if train:
        translation_vector = np.random.rand(3) * 0.01 - 0.005  # 随机平移向量
        sampled_points += translation_vector
    sampled_points = (sampled_points - mean_std_dict["centroid_mean"]) / mean_std_dict[
        "centroid_std"
    ]
    return {
        "centroids": paddle.to_tensor(sampled_points),
        "local_centroid": paddle.to_tensor(local_sampled_points),
        "p_mean": mean_std_dict["press_std"],
        "p_std": mean_std_dict["press_std"],
        "wss_mean": mean_std_dict["wss_mean"],
        "wss_std": mean_std_dict["wss_std"],
    }


class PointCloudDataset(paddle.io.Dataset):
    """
    A dataset class for handling point cloud data.
    Args:
        root_dir (string): The directory containing all the point cloud files.
        train (bool, optional): A flag indicating whether the dataset is for training.
        Defaults to True.
        translate (bool, optional): A flag indicating whether to apply translation
        to the point cloud data during training. Defaults to True.
        test (bool, optional): A flag indicating whether the dataset is for testing.
        Defaults to False.
        num (int, optional): The number of point cloud files to load from the directory.
        Defaults to 1.
    """

    def __init__(self, root_dir, train=True, translate=True, test=False, num=1):
        self.root_dir = root_dir
        # 遍历文件夹
        self.file_list = [
            f for f in os.listdir(root_dir) if f.endswith(".npy") and "centroid" in f
        ]
        # 使用列表推导式过滤掉包含任何子字符串的元素
        substrings_to_remove = ["0978", "1034", "2860", "3641"]
        self.file_list = [
            item
            for item in self.file_list
            if not any(sub in item for sub in substrings_to_remove)
        ]
        # 限制训练集个数
        self.file_list = self.file_list[:num]
        if len(self.file_list) == 0:
            raise RuntimeError(f"No files found in provided {root_dir} directory.")
        self.train = train
        self.translate = translate
        self.test = test

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        file_name = self.file_list[idx]
        file_path = os.path.join(self.root_dir, file_name)
        points = np.load(file_path).astype(np.float32)
        if self.train:
            sample_rate = 0.1
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

        p = np.load(
            os.path.join(self.root_dir, file_name.replace("centroid", "press"))
        ).astype(np.float32)
        press_sample = p[sampled_indices]

        wss = np.load(
            os.path.join(
                self.root_dir, file_name.replace("centroid", "wallshearstress")
            )
        ).astype(np.float32)

        normal = np.load(
            os.path.join(self.root_dir, file_name.replace("centroid", "normal"))
        ).astype(np.float32)

        areas = np.load(
            os.path.join(self.root_dir, file_name.replace("centroid", "area"))
        ).astype(np.float32)
        wss_sample = wss[sampled_indices]

        with open(
            os.path.join(
                self.root_dir,
                file_name.replace("centroid", "info").replace("npy", "json"),
            ),
            "r",
        ) as json_file:
            reference_area = json.load(json_file)["reference_area"]

        sample = {
            **normlalize_input(
                points,
                self.root_dir + "/../mean_std.paddledict",
                sampled_indices,
                self.train,
            ),
            "pressure": press_sample,
            "wss": wss_sample,
            "file_name": file_name,
            "Cd": np.array([0.0]),  # tofix
            "reference_area": reference_area,
            "normal": normal[sampled_indices],
            "areas": areas[sampled_indices],
        }
        return sample


class PointCloudDataModule(BaseDataModule):
    def __init__(self, train_data_dir, test_data_dir, n_train_num, n_test_num):
        """
        PointCloudDataModule class for handling point cloud data.
        Args:
            train_data_dir (str): Path to the directory containing the training data.
            test_data_dir (str): Path to the directory containing the testing data.
            n_train_num (int): Number of training samples to load.
            n_test_num (int): Number of testing samples to load.
        """
        BaseDataModule.__init__(self)
        self.train_data_dir = Path(train_data_dir)
        self.test_data_dir = Path(test_data_dir)
        self.train_data = PointCloudDataset(
            train_data_dir, train=True, test=False, num=n_train_num
        )
        self.test_data = PointCloudDataset(
            test_data_dir, train=False, test=True, num=n_test_num
        )

    def decode(self, data, idx: int) -> paddle.Tensor:
        """
        Decode the input data using the specified decoder index.

        Args:
            data (numpy.ndarray): The input data to be decoded.
            idx (int): Index of the decoder to use for decoding.

        Returns:
            paddle.Tensor: The decoded data as a Paddle Tensor.
        """
        return self.decoder[idx](data.T)
