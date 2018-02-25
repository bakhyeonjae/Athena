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

    def connectPorts(self, source, target, edgeSrcDir='AUTO', edgeTgtDir='AUTO'):
        self.setSourcePort(source, edgeSrcDir)
        self.setTargetPort(target, edgeTgtDir)

    def setSourcePort(self, source, edgeDir='AUTO'):
        self.source = source
        self.source.connectEdge(self, edgeDir)

    def setTargetPort(self, target, edgeDir='AUTO'):
        self.target = target
        self.target.connectEdge(self, edgeDir)
    
    def updateViewPos(self):
        sourcePos = None
        targetPos = None
        if self.source:
            sourcePos = self.source.getView().getPos()
        if self.target:
            targetPos = self.target.getView().getPos()
        self.view.updatePortPos(sourcePos, targetPos)

    def propagateExecutionToSource(self):
        print('{}.propagateExecutionToSource'.format(type(self)))
        self.source.propagateExecution()

    def passToBox(self,data):
        print('{}.passToBox'.format(type(self)))
        self.target.passToBox(data)
