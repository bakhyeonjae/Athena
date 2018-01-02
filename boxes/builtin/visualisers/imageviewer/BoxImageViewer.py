import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox
from framework.datatypes.dataloader import DataLoader

class Box(CommonModuleBox):
    def __init__(self, parent=None, instName = ''):
        self.typeName = type(self)
        super().__init__(parent, 1, 0, instName, self.typeName)

        data_in_port = self.inPorts[0]
        data_in_port.setPortType(DataLoader)

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Run", "desc":"Configure module parameters", "method":self.run}]
        self.setPopupActionList(menus)

    def config(self):
        pass

    def execute(self):
        for pin in self.inPorts:
            data = pin.getData()
 
        #print(data.getData(0,0))
        plt.imshow(data.getData(0,0)[0][0])
        plt.pause(0.001)
        print(data.getData(0,0)[0].shape)

