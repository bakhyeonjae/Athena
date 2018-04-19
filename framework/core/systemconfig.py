
class SystemConfig(object):
    boxDir = ''
    toolRootDir = '../..'

    @classmethod
    def getBoxDir(cls):
        # temporary implementation
        cls.boxDir = '../../boxes'
        return cls.boxDir

    @classmethod
    def getLocalWorkSpaceDir(cls):
        return '/Users/viv3.mac.sec/bakhyeonjae/athena_workspace'

    @classmethod
    def getToolDir(cls):
        return cls.toolRootDir 
