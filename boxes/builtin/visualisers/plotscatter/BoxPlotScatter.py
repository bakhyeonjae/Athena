import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import plotly.plotly as py  # tools to communicate with Plotly's server

import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox

class Box(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = ''):
        self.typeName = type(self)
        super().__init__(parent, inputPort, outputPort, instName, self.typeName)

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"Train", "desc":"Train", "method":self.train},
                 {"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Run", "desc":"Configure module parameters", "method":self.run}]
        self.setPopupActionList(menus)

    def export(self):
        pass

    def train(self):
        pass

    def config(self):
        pass

    def run(self):
        scatter = plt.figure()

        colors = (i + j for j in 'o<.' for i in 'bgrcmyk')
        labels = 'one two three four five six seven eight nine ten'.split()
        x = linspace(0, 2*pi, 3000)
        d = (2+random((2,3000))) * c_[sin(x), cos(x)].T
        lg = []
        for i, l, c  in zip(range(10), labels, colors):
            start, stop = i * 300, (i + 1) * 300
            handle = plot(d[0, start:stop], d[1, start:stop], c, label=l)
            lg.append(handle)
        show()

        plot_url = py.plot_mpl(scatter, filename='mpl-docs/scatter')
