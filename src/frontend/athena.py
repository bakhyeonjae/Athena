from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys
import math
#import trainerboxcnn

from Box import CommonModuleBox

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from boxes.builtin.visualisers.plotscatter import BoxPlotScatter
from boxes.builtin.primitives.genrandom import BoxRandomGenerator
from boxes.builtin.learners.tmpmnist import BoxMNIST

class ModelBox(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = '', typeName = ''):
        super().__init__(parent, inputPort, outputPort, instName, typeName)

class TesterBox(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = '', typeName = ''):
        super().__init__(parent, inputPort, outputPort, instName, typeName)

class OptimizerBox(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = '', typeName = ''):
        super().__init__(parent, inputPort, outputPort, instName, typeName)

class MainWindow(QFrame):
    listBox = []
    selectedBox = None
    compensated_pos = 0
    isConnecting = False
    beginningPort = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        trainer= BoxPlotScatter.Box(self,[1],[],'Dimension Reducer')
        trainer.move(100, 50)
        self.listBox.append(trainer)

        randomGenerator = BoxRandomGenerator.Box(self,[],[1],'random generator')
        randomGenerator.move(100,300)
        self.listBox.append(randomGenerator)

        mnist = BoxMNIST.Box(self,[1],[1],'MNIST')
        mnist.move(100,500)
        self.listBox.append(mnist)
        
        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 580, 700)

        self.penStart = QPen(QColor(255,0,0))
        self.penStart.setWidth(3)        

        self.penEnd = QPen(QColor(0,0,0))
        self.penEnd.setWidth(1)
        self.brushEnd = QBrush(QColor(0, 0, 0, 255))

    def paintEvent(self, eventQPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(self.penStart)        
        qp.setRenderHints(QPainter.Antialiasing, True)
        qp.setPen(self.penEnd)
        qp.setBrush(self.brushEnd)

        arrow_style = 'narrow-long'

        if self.isConnecting:
            qp.drawPolygon(self.createArrowHead(self.beginningPort.getConnection().getSrcCoord(),self.beginningPort.getConnection().getDstCoord(),arrow_style))
            qp.drawLine(self.beginningPort.getConnection().getSrcCoord(),self.beginningPort.getConnection().getDstCoord())        

        # Scan all the output ports to draw connected lines.
        for box in self.listBox:
            for port in box.outPorts:
                if port.isConnected():
                    qp.drawLine(port.getConnection().getSrcCoord(),port.getConnection().getDstCoord())
                    qp.drawPolygon(self.createArrowHead(port.getConnection().getSrcCoord(), port.getConnection().getDstCoord(),arrow_style))
        qp.end()

    def createArrowHead(self,s,d,style):
        arrow_style = {'narrow-long':{'length':30, 'width':5},
                       'wide-long':{'length':30, 'width':20},
                       'narrow-short':{'length':15, 'width':5},
                       'wide-short':{'length':15, 'width':5}}
        polygon = QPolygonF()
        dx = d.x() - s.x()
        dy = d.y() - s.y()
        l = math.sqrt(dx*dx+dy*dy)
        rv = QPointF(s.x()-d.x(),s.y()-d.y())/l   # reverse vector
        nv = QPointF(s.y()-d.y(),d.x()-s.x())/l   # normal vector
        ep = QPointF(d.x(),d.y())                 # end point
        polygon.append(ep)
        polygon.append(ep+arrow_style[style]['length']*rv+arrow_style[style]['width']*nv)
        polygon.append(ep+arrow_style[style]['length']*rv-arrow_style[style]['width']*nv)
        return polygon

    """
    def createPoly(self, n, r, s, d):
        print("CreatePoly", n, r, d.x(), d.y())
        polygon = QPolygonF()
        w = 360/n
        for i in range(n):
            t = w*i
            add_d = self.getDegree(s, d)
            x = r*math.cos(math.radians(t - add_d))
            y = r*math.sin(math.radians(t - add_d))
            if i == 0:
                polygon.append(QPointF(d.x(), d.y()))
            else:
                polygon.append(QPointF(d.x()+x/5, d.y()+y/5))

        return polygon
 
    def getDegree(self, src, dst):
        dx = dst.x() - src.x()
        dy = dst.y() - src.y()
        rads = math.atan2(-dy,dx)
        rads %= 2*math.pi
        degs = math.degrees(rads)
        return degs
    """

    def dragEnterEvent(self, e):
        for box in self.listBox:
            if box.checkPosition(e.pos()):
                self.selectedBox = box

        if self.selectedBox:
            port = self.selectedBox.isConnecting(e.pos())
            if port:
                self.isConnecting = True
                self.beginningPort = port
                self.beginningPort.createConnectionLine()
            else:
                self.compensated_pos = e.pos() - self.selectedBox.pos()

        e.accept()

    def dragMoveEvent(self, e):
        if self.isConnecting:
            self.beginningPort.updateDstPosition(e.pos())
        else:
            position = e.pos()
            self.selectedBox.move(position - self.compensated_pos)
            self.selectedBox.updatePortPos()

        self.update()
        e.accept()

    def dropEvent(self, e):
        if self.isConnecting:
            currBox = None
            port = None
            for box in self.listBox:
                if box.checkPosition(e.pos()):
                    currBox = box

            if currBox:
                port = currBox.isArrived(e.pos())

            if currBox and port and currBox != self.selectedBox and self.beginningPort.checkPortMatch(port):
                self.beginningPort.connectPort(port)
            else:
                self.beginningPort.deleteConnectionLine()
            self.isConnecting = False
            
        self.selectedBox = None
        self.update()

        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == "__main__":
    # check if QApplication already exists
    app = QApplication.instance()
    if not app:     # create QApplication if it doesnt exist
        app = QApplication(sys.argv)
    mywin = MainWindow()
    mywin.show()
    sys.exit(app.exec_())
