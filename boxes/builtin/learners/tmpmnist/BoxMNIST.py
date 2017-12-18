import numpy as np
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

class MnistModel(nn.Module):
    def __init__(self):
        super(MnistModel, self).__init__()
        # input is 28x28
        # padding=2 for same padding
        self.conv1 = nn.Conv2d(1, 32, 5, padding=2)
        # feature map size is 14*14 by pooling
        # padding=2 for same padding
        self.conv2 = nn.Conv2d(32, 64, 5, padding=2)
        # feature map size is 7*7 by pooling
        self.fc1 = nn.Linear(64*7*7, 1024)
        self.fc2 = nn.Linear(1024, 10)
        
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, 64*7*7)   # reshape Variable
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)

class Box(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = ''):
        self.typeName = type(self)
        super().__init__(parent, inputPort, outputPort, instName, self.typeName)

        self.dim = [100,2]
        self.randType = 'uniform'

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"Train", "desc":"Train", "method":self.train},
                 {"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Run", "desc":"Configure module parameters", "method":self.run}]
        self.setPopupActionList(menus)

    def export(self):
        pass

    def train(self):
        pass

    def config(self):
        pass

    def execute(self):

        model = MnistModel()

        batch_size = 50
        train_loader = torch.utils.data.DataLoader(datasets.MNIST('data', train=True, download=True, transform=transforms.ToTensor()), batch_size=batch_size, shuffle=True)
        test_loader = torch.utils.data.DataLoader(datasets.MNIST('data', train=False, transform=transforms.ToTensor()), batch_size=1000)

        for p in model.parameters():
            print(p.size())

        optimizer = optim.Adam(model.parameters(), lr=0.0001)

        model.train()
        train_loss = []
        train_accu = []
        i = 0
        for epoch in range(15):
            for data, target in train_loader:
                data, target = Variable(data), Variable(target)
                optimizer.zero_grad()
                output = model(data)
                loss = F.nll_loss(output, target)
                loss.backward()    # calc gradients
                train_loss.append(loss.data[0])
                optimizer.step()   # update gradients
                prediction = output.data.max(1)[1]   # first column has actual prob.
                accuracy = prediction.eq(target.data).sum()/batch_size*100
                train_accu.append(accuracy)
                if i % 1000 == 0:
                    print('Train Step: {}\tLoss: {:.3f}\tAccuracy: {:.3f}'.format(i, loss.data[0], accuracy))
                i += 1

        plt.plot(np.arange(len(train_loss)), train_loss)
        plt.plot(np.arange(len(train_accu)), train_accu)

        model.eval()
        correct = 0
        for data, target in test_loader:
            data, target = Variable(data, volatile=True), Variable(target)
            output = model(data)
            prediction = output.data.max(1)[1]
            correct += prediction.eq(target.data).sum()

        print('\nTest set: Accuracy: {:.2f}%'.format(100. * correct / len(test_loader.dataset)))

        self.data = np.random.rand(self.dim[0],self.dim[1])

        for port in self.outPorts:
            port.transferData(self.data)
