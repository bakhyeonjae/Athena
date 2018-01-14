class randomgen(object):
    def __init__(self):
        pass

    def execute(self, mean, variance):
        print('#####3  {}.{}'.format(mean,variance))
        dim = [900,2]
        self.data = np.random.rand(dim[0],dim[1])

        return self.data
