""" This module is mainly for TrainerBox class.

"""

from PySide.QtGui import *
from PySide.QtCore import *
import sys
import athena

class TrainerBox(athena.CommonModuleBox):
    """ This class displays a module for training. 
    """
    def __init__(self, parent=None):
        athena.CommonModuleBox.__init__(self, parent)
        self.setText('CNN Trainer')

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"train", "desc":"Train", "method":self.train},
                 {"title":"config", "desc":"Configure module parameters", "method":self.config}]
        self.setPopupActionList(menus)

    def export(self):
        print("Export!")

    def train(self):
        print("Train begin!")

    def config(self):
        print("Config!")

