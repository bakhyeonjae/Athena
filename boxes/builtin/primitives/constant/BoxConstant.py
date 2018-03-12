import numpy as np

class Constant(object):
    def __init__(self):
        pass

    def execute(self,val):
        self.data = float(val)
