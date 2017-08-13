""" This module is mainly for TrainerBox class.

"""

from PySide.QtGui import *
from PySide.QtCore import *
import sys
import athena

class OptimizerBox(athena.CommonModuleBox):
    """ This class displays a module for optimization.
    """
    popupActions = [];  # list of dictionary, Key :"title","desc","method"

    def __init__(self, parent=None):
        # athena.CommonModuleBox.__init__(self, parent)
        super(OptimizerBox, self).__init__(parent)
        self.setText('CNN Optimizer')

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title": "Export",    "desc": "Export",   "method": self.export   },
                 {"title": "Compile",   "desc": "Compile",  "method": self.compile  },
                 {"title": "Fit",       "desc": "Fit",      "method": self.fit      },
                 {"title": "Optimize",  "desc": "Optimize", "method": self.optimize }]
        self.setPopupActionList(menus)

    def setPopupActionList(self, menuList):
        for menu in menuList:
            if menu not in self.popupActions:
                self.popupActions.append(menu)

    def export(self):
        print("Export!")

    def compile(self):
        print("Compile!")

    def fit(self):
        print("Fit!")

    def optimize(self):
        print("Optimize!")
