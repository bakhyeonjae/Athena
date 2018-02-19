import sys

sys.path.append('../..')

from src.frontend.edgeview import EdgeView

class Edge(object):
    def __init__(self):
        self.source = None
        self.target = None
        self.view = EdgeView(self)

    def setSrcCoord(self, pos):
        self.view.setSrcCoord(pos)
   
    def setDstCoord(self, pos):
        self.view.setDstCoord(pos)

    def getView(self):
        return self.view

    def connectPorts(self, source, target):
        self.setSourcePort(source)
        self.setTargetPort(target)

    def setSourcePort(self, source):
        self.source = source
        self.source.connectEdge(self)

    def setTargetPort(self, target):
        self.target = target
        self.target.connectEdge(self)
    
    def updateViewPos(self):
        sourcePos = None
        targetPos = None
        if self.source:
            sourcePos = self.source.getView().getPos()
        if self.target:
            targetPos = self.target.getView().getPos()
        self.view.updatePortPos(sourcePos, targetPos)

    def propagateExecutionToSource(self):
        self.source.propagateExecution()

    def passToBox(self,data):
        self.target.passToBox(data)
