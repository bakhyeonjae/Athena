import torch
from torchvision import datasets, transforms
from torch.autograd import Variable

import numpy

class DataLoader(object):
    def __init__(self):
        self.dataset = datasets.MNIST('data', train=False, download=True, transform=transforms.ToTensor())

    def length(self):
        return len(self.dataset)

    def getData(self, idx, num):
        data_list = []
        data_list.append(Variable((self.dataset[idx][0])).data.numpy())
        return data_list
