import torch.nn as nn
from .utils import auto_infer
from .trainer import Trainer
from .rl import RLModel
from .gan import GANModel
import torch

class NeuralNet(nn.Sequential):
    def __init__(self, *layers):
        super().__init__()
        for idx, layer in enumerate(layers):
            self.add_module(f"layer_{idx}", layer.layer)

    def build(self, input_shape=(1, 28, 28)):
        auto_infer(self, input_shape)
        return self

    def compile(self, optimizer='Adam', lr=0.001, loss='CrossEntropyLoss', device=None):
        input_shape = getattr(self, 'input_shape', (1, 28, 28))
        self.build(input_shape=input_shape)  # 自动构建模型结构
        from .trainer import Trainer
        self.trainer = Trainer(self, optimizer=optimizer, lr=lr, loss=loss, device=device)
        return self

    def fit(self, dataset='mnist', epochs=5, batch_size=64, verbose=True, device=None):
        self.trainer.fit(dataset=dataset, epochs=epochs, batch_size=batch_size, verbose=verbose, device=device)

    def plot(self):
        self.trainer.plot_loss()

    def save(self, path="model.pth"):
        torch.save(self.state_dict(), path)
        print(f"Model saved to {path}")

    def load(self, path="model.pth"):
        """从文件加载模型状态字典"""
        state_dict = torch.load(path)
        self.load_state_dict(state_dict)
        print(f"Model loaded from {path}")
        return self  # 返回自身以支持链式调用

    def load_if_exists(self, path="model.pth"):
        if os.path.exists(path):
            print(f"Loading existing model from {path}")
            self.load(path)
        else:
            print("No model found, proceeding with new model.")
        return self

    @classmethod
    def RL(cls, env_name='CartPole-v1', policy='MLP', hidden_dim=128):
        return RLModel(env_name, policy, hidden_dim)

    @classmethod
    def GAN(cls, latent_dim=100, img_shape=(1, 28, 28), generator=None, discriminator=None):
        return GANModel(latent_dim, img_shape, generator, discriminator)

    @property
    def device(self):
        """返回模型所在的设备"""
        return next(self.parameters()).device