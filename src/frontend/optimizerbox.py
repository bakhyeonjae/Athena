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

# # The following code is a simple training example written in Keras.
#
# from keras.models import Sequential
# from keras.layers import Dense, Activation
#
# model = Sequential()
#
# model.add(Dense(units=64, input_dim=100))
# model.add(Activation('relu'))
# # model.add(Dense(units=1))
# model.add(Dense(units=10))
# model.add(Activation('softmax'))
#
# # model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
# # model.compile(loss=keras.losses.categorical_crossentropy , optimizer=keras.optimizer.SGD(lr=0.01, momentum=0.9, nesterov=True))
#
# import numpy as np
#
# data = np.random.random((1000, 100))
# # data = np.random.randint(2, size=(1000, 1))
# labels = np.random.randint(10, size=(1000, 1))
#
# import keras.utils
# one_hot_labels = keras.utils.to_categorical(labels, num_classes=10)
#
# # model.fit(data, label, epochs=5, batch_size=32)
# model.fit(data, one_hot_labels, epochs=10, batch_size=32)
