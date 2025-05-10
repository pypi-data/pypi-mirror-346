import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class Generator(nn.Module):
    def __init__(self, latent_dim, img_shape):
        super().__init__()
        self.img_shape = img_shape
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, int(torch.prod(torch.tensor(img_shape)))),
            nn.Tanh()
        )

    def forward(self, z):
        img = self.model(z)
        return img.view(img.size(0), *self.img_shape)

class Discriminator(nn.Module):
    def __init__(self, img_shape):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(int(torch.prod(torch.tensor(img_shape))), 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, img):
        img_flat = img.view(img.size(0), -1)
        return self.model(img_flat)

class GANModel:
    def __init__(self, latent_dim=100, img_shape=(1, 28, 28), generator=None, discriminator=None):
        self.latent_dim = latent_dim
        self.generator = generator or Generator(latent_dim, img_shape)
        self.discriminator = discriminator or Discriminator(img_shape)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.generator.to(self.device)
        self.discriminator.to(self.device)
        self.optimizer_G = optim.Adam(self.generator.parameters(), lr=0.0002)
        self.optimizer_D = optim.Adam(self.discriminator.parameters(), lr=0.0002)
        self.adversarial_loss = nn.BCELoss()

    def train_step(self, real_images):
        batch_size = real_images.size(0)
        valid = torch.ones(batch_size, 1).to(self.device)
        fake = torch.zeros(batch_size, 1).to(self.device)

        # ---------------------
        #  训练判别器
        # ---------------------
        self.optimizer_D.zero_grad()
        real_loss = self.adversarial_loss(self.discriminator(real_images), valid)
        z = torch.randn(batch_size, self.latent_dim).to(self.device)
        fake_images = self.generator(z)
        fake_loss = self.adversarial_loss(self.discriminator(fake_images.detach()), fake)
        d_loss = (real_loss + fake_loss) / 2
        d_loss.backward()
        self.optimizer_D.step()

        # ---------------------
        #  训练生成器
        # ---------------------
        self.optimizer_G.zero_grad()
        g_loss = self.adversarial_loss(self.discriminator(fake_images), valid)
        g_loss.backward()
        self.optimizer_G.step()

        return d_loss.item(), g_loss.item()