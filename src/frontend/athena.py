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
        randomGenerator.move(200,50)
        self.listBox.append(randomGenerator)

        model= ModelBox(self,[1,2],[1,1,1],'Test Module','NN.CNN')
        model.move(100, 200)
        self.listBox.append(model)

        tester = TesterBox(self,[1],[1],'MNIST loader','Generator.ImageLoader')
        tester.move(100, 350)
        self.listBox.append(tester)

        optimizer = OptimizerBox(self,[1],[1],'Data generator','Generator.Random')
        optimizer.move(100, 500)
        self.listBox.append(optimizer)

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
        if self.isConnecting:
            qp.drawLine(self.beginningPort.getConnection().getSrcCoord(),self.beginningPort.getConnection().getDstCoord())        

        # Scan all the output ports to draw connected lines.
        for box in self.listBox:
            for port in box.outPorts:
                if port.isConnected():
                    qp.setPen(self.penEnd)
                    qp.setBrush(self.brushEnd)
                    qp.drawLine(port.getConnection().getSrcCoord(),port.getConnection().getDstCoord())
                    self.ploygon = self.createPoly(3, 60, port.getConnection().getSrcCoord(), port.getConnection().getDstCoord())
                    qp.drawPolygon(self.ploygon)

        qp.end()

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
                polygon.append(QPointF(d.x()+x/3, d.y()+y/3))

        return polygon
    
    def getDegree(self, src, dst):
        dx = dst.x() - src.x()
        dy = dst.y() - src.y()
        rads = math.atan2(-dy,dx)
        rads %= 2*math.pi
        degs = math.degrees(rads)
        return degs

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
