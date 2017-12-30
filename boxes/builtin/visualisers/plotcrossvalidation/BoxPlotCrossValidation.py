import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, sys, inspect
import itertools

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox

class Box(CommonModuleBox):
    _getId = itertools.count()

    def __init__(self, parent=None, instName = ''):
        self.typeName = type(self)
        super().__init__(parent, 2, 0, instName, self.typeName)

        self.trainErrorPort = self.inPorts[0]
        self.trainErrorPort.setPortType(list)
        self.testErrorPort= self.inPorts[1]
        self.testErrorPort.setPortType(list)
        self.idxFig = next(self._getId)
        self.enableWindow = True

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Open the window", "desc":"Configure module parameters", "method":self.openWindow},
                 {"title":"Close the window", "desc":"Configure module parameters", "method":self.closeWindow}]
        self.setPopupActionList(menus)

    def config(self):
        pass

    def execute(self):
        plt.figure(self.idxFig)
        plt.ion()
        plt.show()

    def openWindow(self):
        self.enableWindow = True

    def closeWindow(self):
        self.enableWindow = False

    def update(self):
        
        if (self.enableWindow):
            train_error_rate = self.trainErrorPort.getData()
            test_error_rate = self.testErrorPort.getData()
            fig = plt.figure(self.idxFig)
            fig.canvas.set_window_title(self.instName)
            if train_error_rate:
                plt.plot(train_error_rate)
            if test_error_rate:
                plt.plot(test_error_rate)
            plt.draw()

        plt.pause(0.001)


