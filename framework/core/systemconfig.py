
class SystemConfig(object):
    boxDir = ''

    @classmethod
    def getBoxDir(cls):
        # temporary implementation
        cls.boxDir = '../../boxes'
        return cls.boxDir
