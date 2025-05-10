import torch
import matplotlib.pyplot as plt

def auto_infer(model, input_shape=(1, 28, 28)):
    with torch.no_grad():
        dummy = torch.zeros(1, *input_shape)
        for module in model:
            dummy = module(dummy)
    return model

def register_activation_hook(model):
    """注册钩子以获取每层的输出"""
    activations = []

    def hook(module, input, output):
        activations.append(output.detach().cpu())

    hooks = []
    for name, module in model.named_children():
        hooks.append(module.register_forward_hook(hook))
    return activations, hooks

def plot_activations(activations):
    for i, act in enumerate(activations):
        plt.figure(figsize=(10, 4))
        plt.hist(act.view(-1).numpy(), bins=50)
        plt.title(f"Layer {i+1} Activation Distribution")
        plt.xlabel("Activation Value")
        plt.ylabel("Frequency")
        plt.show()

