import numpy as np

class Concat3(object):
    def __init__(self):
        pass

    def execute(self,in1,in2,in3):
        self.data = np.concatenate((in1,in2,in3))
