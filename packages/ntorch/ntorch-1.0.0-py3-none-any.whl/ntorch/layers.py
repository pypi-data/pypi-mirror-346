
import torch.nn as nn

class Layer:
    def __init__(self, layer_type, *args, **kwargs):
        if not hasattr(nn, layer_type) and layer_type != "Flatten":
            raise ValueError(f"Unsupported layer type: {layer_type}")
        
        if layer_type == "Flatten":
            self.layer = Flatten(*args, **kwargs)
        else:
            self.layer = getattr(nn, layer_type)(*args, **kwargs)

class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.size(0), -1)