import torch
import matplotlib.pyplot as plt
from ntorch.data import get_dataloader
from ntorch.config import default_config

class Trainer:
    def __init__(self, model, optimizer='Adam', lr=0.001, loss='CrossEntropyLoss', device=None):
        self.model = model
        self.optimizer_name = optimizer
        self.lr = lr
        self.loss_name = loss
        self.criterion = getattr(torch.nn, loss)()
        self.optimizer = getattr(torch.optim, optimizer)(model.parameters(), lr=lr)
        self.val_losses = []
        self.accuracies = []

        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        self.model.to(self.device)
        self.train_losses = []

    def fit(self, dataset='mnist', epochs=None, batch_size=None, verbose=True, device=None):
        """
        训练模型，支持指定设备、数据集、轮数和批量大小。
        """
        # 使用 Config 中的默认参数，允许覆盖
        epochs = epochs or default_config.epochs
        batch_size = batch_size or default_config.batch_size

        # 更新 device（优先级：函数参数 > 初始化参数 > 全局配置）
        current_device = device or str(self.device)

        if current_device != str(self.device):
            self.device = torch.device(current_device)
            self.model.to(self.device)

        # 加载数据
        train_loader, val_loader = get_dataloader(
            dataset,
            batch_size=batch_size,
            root=default_config.dataset_root,
            download=default_config.download_dataset
        )

        for epoch in range(epochs):
            # 训练阶段
            self.model.train()
            total_loss = 0
            for images, labels in train_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()

            avg_loss = total_loss / len(train_loader)
            self.train_losses.append(avg_loss)

            # 验证阶段
            self.model.eval()
            with torch.no_grad():
                val_loss = 0
                correct = 0
                total = 0
                for images, labels in val_loader:
                    images, labels = images.to(self.device), labels.to(self.device)
                    outputs = self.model(images)
                    val_loss += self.criterion(outputs, labels).item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()

                val_loss /= len(val_loader)
                accuracy = 100 * correct / total
                self.val_losses.append(val_loss)
                self.accuracies.append(accuracy)

            if verbose:
                print(f"Epoch [{epoch+1}/{epochs}], "
                      f"Train Loss: {avg_loss:.4f}, "
                      f"Val Loss: {val_loss:.4f}, "
                      f"Accuracy: {accuracy:.2f}%")

    def plot_loss(self):
        import numpy as np
        smoothed = np.convolve(self.train_losses, np.ones(5)/5, mode='valid')
        plt.plot(smoothed, label="Smoothed Training Loss")
        plt.plot(self.train_losses, alpha=0.3, label="Raw Loss")
        plt.legend()
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Training Loss Curve")
        plt.show()