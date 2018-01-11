import numpy as np
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir) 
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox
from src.frontend.Port import PortIn
from boxes.private.MyFirstBox.boxloader import BoxLoader

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from framework.dialog.ConfigDialog import ConfigDialog

class Box(CommonModuleBox):
    def __init__(self, parent=None, instName = ''):
        loader = BoxLoader()
        with open('../../boxes/private/MyFirstBox/BoxRandomLabeled.box','r') as f:
            data = f.read()
            box = loader.loadBoxDesc(data)
            for subbox in box['sub-box']:
                loader.createBox(parent,subbox)
                parent.addBox(subbox)
        #super().__init__(parent, 0, 1, instName, self.typeName)

    def configPopupMenu(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Run", "desc":"Configure module parameters", "method":self.run}]
        self.setPopupActionList(menus)

    def export(self):
        pass

    def train(self):
        pass

    def config(self):
        dimension, ok = ConfigDialog.getParameters()
        self.dim[1] = dimension

    def execute(self):
        self.data = np.random.rand(self.dim[0],self.dim[1])

        for port in self.outPorts:
            port.transferData(self.data)
