""" This module is mainly for TrainerBox class.

"""

from PySide.QtGui import *
from PySide.QtCore import *
import sys
import athena

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from controltower import cnn
import trainerbox

class TrainerBoxCNN(trainerbox.TrainerBox):
    """ This class displays a module for training. 
    """
    def __init__(self, parent=None):
        trainerbox.TrainerBox.__init__(self,parent)
        self.setText('CNN Trainer')

    def export(self):
        print("Export!")

    def train(self):
        print("Train begin!")

    def config(self):
        print("Config!")

