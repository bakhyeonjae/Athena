
class EdgeView(object):
    def __init__(self, core):
        self.core = core

    def updatePortPos(self, source, target):
        self.setSrcCoord(source)
        self.setDstCoord(target)

    def setSrcCoord(self, pos):
        self.srcPos = pos

    def setDstCoord(self, pos):
        self.dstPos = pos

    def getSrcCoord(self):
        return self.srcPos

    def getDstCoord(self):
        return self.dstPos
