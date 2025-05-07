import torch
from torch.utils.data import DataLoader

def get_mean_and_std(train_data):
    train_loader = DataLoader(
        train_data, batch_size=1, shuffle=False, num_workers=0,
        pin_memory=True)
    mean = torch.zeros(3)
    std = torch.zeros(3)
    for im, _ in train_loader:
        for d in range(3):
            mean[d] += im[:, d, :, :].mean()
            std[d] += im[:, d, :, :].std()
    mean.div_(len(train_data))
    std.div_(len(train_data))
    return list(mean.numpy()), list(std.numpy())