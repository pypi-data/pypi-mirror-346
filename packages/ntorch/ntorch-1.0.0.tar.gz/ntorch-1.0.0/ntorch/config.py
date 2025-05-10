import os
import torch

class Config:
    def __init__(self):

        self.verbose = True              # 是否打印训练日志
        self.device = self._get_device() # 自动选择设备（GPU or CPU）


        self.epochs = 10                 # 默认训练轮数
        self.batch_size = 64             # 默认 batch size
        self.lr = 0.001                  # 默认学习率
        self.optimizer = 'Adam'          # 默认优化器
        self.loss_function = 'CrossEntropyLoss'  # 默认损失函数


        self.dataset_root = './data'     # 数据集根目录
        self.download_dataset = True     # 是否自动下载数据集


        self.default_model_path = './models/model.pth'  # 默认模型保存路径
        self.save_best_only = True       # 是否只保存最佳模型


        self.rl_episodes = 200           # 默认强化学习 episode 数量
        self.rl_hidden_dim = 128         # 默认策略网络隐藏层维度


        self.gan_latent_dim = 100        # GAN 的潜在空间维度
        self.gan_img_shape = (1, 28, 28) # 图像形状（如 MNIST）


        self.plot_loss_curve = True      # 是否绘制 loss 曲线

    def _get_device(self):
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif hasattr(torch, 'version') and hasattr(torch.version, 'hip'):
            return torch.device("cuda")  # ROCm 使用 cuda 作为后端名
        else:
            return torch.device("cpu")

    def update(self, **kwargs):
        """动态更新配置项"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise KeyError(f"Invalid config key: {key}")

    def show(self):
        """显示当前配置信息"""
        print("=== ntorch Configuration ===")
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
        print("=============================")


default_config = Config()