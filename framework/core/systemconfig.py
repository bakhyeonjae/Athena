
class SystemConfig(object):
    boxDir = ''
    toolRootDir = '../..'

    @classmethod
    def getBoxDir(cls):
        # temporary implementation
        cls.boxDir = '../../boxes'
        return cls.boxDir

    @classmethod
    def getToolDir(cls):
        return cls.toolRootDir 
