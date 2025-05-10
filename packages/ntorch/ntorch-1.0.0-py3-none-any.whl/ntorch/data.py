from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def get_dataloader(name='mnist', batch_size=64, root='./data', download=True):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    if name.lower() == 'mnist':
        train = datasets.MNIST(root=root, train=True, download=download, transform=transform)
        test = datasets.MNIST(root=root, train=False, download=download, transform=transform)
    elif name.lower() == 'fashionmnist':
        train = datasets.FashionMNIST(root=root, train=True, download=download, transform=transform)
        test = datasets.FashionMNIST(root=root, train=False, download=download, transform=transform)
    elif name.lower() == 'cifar10':
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        train = datasets.CIFAR10(root=root, train=True, download=download, transform=transform)
        test = datasets.CIFAR10(root=root, train=False, download=download, transform=transform)
    else:
        raise ValueError(f"Dataset '{name}' is not supported yet.")

    train_loader = DataLoader(train, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader