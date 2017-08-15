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

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"train", "desc":"Train", "method":self.train},
                 {"title":"config", "desc":"Configure module parameters", "method":self.config}]
        self.setPopupActionList(menus)

    def export(self):
        pass

    def train(self):
        pass

    def config(self):
        pass

