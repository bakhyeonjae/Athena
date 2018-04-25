import numpy as np

class Shuffle(object):
    def __init__(self):
        pass

    def execute(self,datain):
        np.random.shuffle(datain)
        self.dataout = datain
