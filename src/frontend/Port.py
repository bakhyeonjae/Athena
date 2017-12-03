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
    connection = None

    def __init__(self, parent):
        Port.__init__(self,parent)
        self.setStyleSheet("QLabel { background-color:blue; color:black; border:1px solid white}")

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData(self)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)

    
class PortOut(Port):
    data = None
    connection = None
    parent = None

    def __init__(self,parent):
        Port.__init__(self,parent)
        self.parent = parent
        self.setStyleSheet("QLabel {background-color:red; color:black; border:1px solid white}")

    def setData(self, data):
        self.data = data

    def createConnectionLine(self):
        self.connection = Connection()
        self.connection.setSrcCoord(self.pos() + self.parent.pos())

    def updateDstPosition(self, pos):
        self.connection.setDstCoord(pos)

    def getConnection(self):
        return self.connection

    def deleteConnectionLine(self):
        self.connection = None

