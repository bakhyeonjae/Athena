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
        super().__init__(parent, 1, 0, instName, self.typeName)

        self.dataInPort = self.inPorts[0]
        self.dataInPort.setPortType(list)
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
            data = self.dataInPort.getData()
            fig = plt.figure(self.idxFig)
            fig.canvas.set_window_title(self.instName)
            plt.plot(data)
            plt.draw()

        plt.pause(0.001)


