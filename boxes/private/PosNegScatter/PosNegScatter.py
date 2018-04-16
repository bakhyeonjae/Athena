import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, sys, inspect

class PosNegScatter(object):
    def __init__(self):
        pass

    def execute(self,pos_data,neg_data):
        fig = plt.figure()
        if pos_data.shape[1] == 2:
            ax = fig.subplots()
            ax.scatter(pos_data[:,0],pos_data[:,1], color='b')
            ax.scatter(neg_data[:,0],neg_data[:,1], color='r')
        plt.show()
