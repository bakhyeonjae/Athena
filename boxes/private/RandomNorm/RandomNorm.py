import numpy as np

class RandomNorm(object):
    def __init__(self):
        self.dim = 2
        self.sample = 100
        pass

    def execute(self,mean,variance,dim=2,sample=100):
        dimension = [int(sample),int(dim)]
        self.data = np.random.normal(loc=mean,scale=variance,size=(dimension[0],dimension[1]))
