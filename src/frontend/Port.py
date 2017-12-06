from PySide.QtGui import *
from PySide.QtCore import *
import sys

class Port(QLabel):
    dataType = None

    def __init__(self, parent=None):
        QLabel.__init__(self,parent)

    def setPortType(self, portType, dataType):
        self.dataType = dataType

    def checkPosition(self, pos):
        if pos.x() < self.pos().x():
            return False
        if pos.x() > self.pos().x() + self.width():
            return False
        if pos.y() < self.pos().y():
            return False
        if pos.y() > self.pos().y() + self.height():
            return False

        return True

class Connection(object):
    coordSrc = None
    coordDst = None

    def setSrcCoord(self, pos):
        self.coordSrc = pos

    def setDstCoord(self, pos):
        self.coordDst = pos

    def getSrcCoord(self):
        return self.coordSrc

    def getDstCoord(self):
        return self.coordDst

class PortIn(Port):
    
    def __init__(self, parent):
        Port.__init__(self,parent)
        self.connectedTo = None
        self.parent = parent
        self.setStyleSheet("QLabel { background-color:blue; color:black; border:1px solid white}")

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData(self)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)

    def connectPort(self,portOut):
        self.connectedTo = portOut

    def isConnected(self):
        if self.connectedTo:
            return True
        else:
            return False

    def getConnection(self):
        if self.connectedTo:
            return self.connectedTo.getConnection()
        else:
            return None
    
class PortOut(Port):

    def __init__(self,parent):
        Port.__init__(self,parent)
        self.data = None
        self.connection = None
        self.connectedTo = None
        self.parent = parent
        self.setStyleSheet("QLabel {background-color:red; color:black; border:1px solid white}")

    def setData(self, data):
        self.data = data

    def createConnectionLine(self):
        self.connection = Connection()
        self.connection.setSrcCoord(QPoint(self.pos().x()+self.width()/2,self.pos().y()+self.height()/2) + self.parent.pos())

    def updateDstPosition(self, pos):
        self.connection.setDstCoord(pos)

    def getConnection(self):
        return self.connection

    def deleteConnectionLine(self):
        self.connection = None

    def checkPortMatch(self,portIn):
        if self.dataType == portIn.dataType:
            return True
        else:
            return False

    def isConnected(self):
        if self.connectedTo:
            return True
        else:
            return False
            
    def connectPort(self,portIn):
        self.connectedTo = portIn
        portIn.connectPort(self)

    def disconnectPort(self):
        self.connectedTo = None

