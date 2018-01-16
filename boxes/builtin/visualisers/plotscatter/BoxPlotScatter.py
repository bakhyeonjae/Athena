import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, sys, inspect

class PlotScatter(object):
    def __init__(self):
        pass

    def execute(self, points):
        fig = plt.figure()
        if points.shape[1] == 2:
            ax = fig.subplots()
            ax.scatter(points[:,0],points[:,1])
        elif points.shape[1] == 3:
            ax = fig.add_subplot(111,projection='3d')
            ax.scatter(points[:,0],points[:,1],points[:,2])
        
        plt.show()

