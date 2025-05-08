import torch

class Dataset:
    def __init__(self, images, features, masks):
        self.images = torch.tensor(images, dtype = torch.float32).permute((0, 3, 1, 2))
        self.masks = torch.tensor(masks, dtype = torch.float32).unsqueeze(1)
        self.features = torch.tensor(features, dtype = torch.float32)
