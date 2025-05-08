import os

import numpy as np
import paddle

from src.data.base_datamodule import BaseDataModule


class PDE_Cylinder_DataModule(BaseDataModule):
    def __init__(
        self,
        train_data_dir,
        test_data_dir,
        n_train,
        n_test,
        downsamplex=1,
        downsampley=1,
    ):
        BaseDataModule.__init__(self)
        n_train = max(n_train, 1000)
        n_test = max(n_train, 200)
        INPUT_X = train_data_dir + "/NACA_Cylinder_X.paddletensor"
        INPUT_Y = train_data_dir + "/NACA_Cylinder_Y.paddletensor"
        OUTPUT_Sigma = train_data_dir + "/NACA_Cylinder_Q.paddletensor"
        r1 = downsamplex  # x downsample resolution
        r2 = downsampley  # y downsample resolution
        s1 = int((221 - 1) / r1 + 1)
        s2 = int((51 - 1) / r2 + 1)
        inputX = paddle.load(INPUT_X).astype("float32")
        inputY = paddle.load(INPUT_Y).astype("float32")
        input_tensor = paddle.stack(x=[inputX, inputY], axis=-1)

        # Convert data into tensor
        output_data = paddle.load(OUTPUT_Sigma)
        output_tensor = output_data[:, 4].astype("float32")

        # Train
        x_train = input_tensor[:n_train, ::r1, ::r2][:, :s1, :s2]
        y_train = output_tensor[:n_train, ::r1, ::r2][:, :s1, :s2]
        x_train = x_train.reshape(n_train, -1, 2)
        y_train = y_train.reshape(n_train, -1)
        self.train_data = paddle.io.TensorDataset([x_train, x_train, y_train])

        # Test
        x_test = input_tensor[n_train : n_train + n_test, ::r1, ::r2][:, :s1, :s2]
        y_test = output_tensor[n_train : n_train + n_test, ::r1, ::r2][:, :s1, :s2]
        x_test = x_test.reshape(n_test, -1, 2)
        y_test = y_test.reshape(n_test, -1)
        self.test_data = paddle.io.TensorDataset([x_test, x_test, y_test])
