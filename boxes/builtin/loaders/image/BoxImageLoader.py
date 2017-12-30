import numpy as np
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir) 

from Aspecter import Aspecter

parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox

import torch
from torchvision import datasets, transforms

class Box(CommonModuleBox):
    def __init__(self, parent=None, instName = ''):
        self.typeName = type(self)
        super().__init__(parent, 0, 1, instName, self.typeName)

        data_port = self.outPorts[0]
        data_port.setPortType(torch.utils.data.dataloader.DataLoader)

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Run", "desc":"Configure module parameters", "method":self.run}]
        self.setPopupActionList(menus)

    def export(self):
        pass

    def config(self):
        pass

    def execute(self):

        batch_size = 50
        train_loader = torch.utils.data.DataLoader(datasets.MNIST('data', train=True, download=True, transform=transforms.ToTensor()), batch_size=batch_size, shuffle=True)

        self.data = train_loader

        for port in self.outPorts:
            port.transferData(self.data)

class BoxTest(CommonModuleBox):
    def __init__(self, parent=None, instName = ''):
        self.typeName = type(self)
        super().__init__(parent, 0, 1, instName, self.typeName)

        data_port = self.outPorts[0]
        data_port.setPortType(torch.utils.data.dataloader.DataLoader)

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Run", "desc":"Configure module parameters", "method":self.run}]
        self.setPopupActionList(menus)

    def export(self):
        pass

    def config(self):
        pass

    def execute(self):

        batch_size = 200
        train_loader = torch.utils.data.DataLoader(datasets.MNIST('data', train=False, download=True, transform=transforms.ToTensor()), batch_size=batch_size, shuffle=True)

        self.data = train_loader

        for port in self.outPorts:
            port.transferData(self.data)
