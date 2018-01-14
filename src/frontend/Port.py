from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys

class ViewPort(QLabel):

    def __init__(self, parent=None):
        QLabel.__init__(self,parent)
        self.dataType = None

    def setPortType(self, dataType):
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

    def setSrcCoord(self, pos):
        self.coordSrc = pos

    def setDstCoord(self, pos):
        self.coordDst = pos

    def getSrcCoord(self):
        return self.coordSrc

    def getDstCoord(self):
        return self.coordDst

class ViewPortIn(ViewPort):
    
    def __init__(self, parent):
        ViewPort.__init__(self,parent)
        self.connectedTo = None
        self.parent = parent
        self.data = None
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

    def disconnectPort(self):
        self.connectedTo = None

    def isConnected(self):
        if self.connectedTo:
            return True
        else:
            return False

    def getConnection(self):
        # Connection is created by output port object. So, do not delete on input port.
        if self.connectedTo:
            return self.connectedTo.getConnection()
        else:
            return None

    def propagateExecution(self):
        if self.connectedTo:
            self.connectedTo.propagateExecution()

    def passToBox(self,data):
        self.data = data

    def getData(self):
        return self.data

    def driveBox(self):
        self.parent.update()        
    
class ViewPortOut(ViewPort):

    def __init__(self,parent):
        ViewPort.__init__(self,parent)
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

    def propagateExecution(self):
        self.parent.run()

    def transferData(self,data):
        if self.connectedTo:
            self.connectedTo.passToBox(data)

    def driveForward(self):
        self.connectedTo.driveBox() 
            
