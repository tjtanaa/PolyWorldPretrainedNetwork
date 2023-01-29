import torch
from torch.utils.data import DataLoader

from dataloader_crowdai import LandsDInferenceDataset

import matplotlib.pyplot as plt
images_directory = "dataset/ESRI_COOR"

LandsD_dataset = LandsDInferenceDataset(images_directory=images_directory)
dataloader = DataLoader(LandsD_dataset, batch_size=2, shuffle=False, num_workers=2)

for sample_batched in dataloader:
    print(sample_batched['image'].shape)
    plt.imshow(sample_batched['image'][0].permute(1,2,0))
    plt.show()
    exit()

