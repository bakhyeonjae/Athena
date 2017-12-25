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
from boxes.builtin.loaders.image import BoxImageLoader
from boxes.builtin.learners.models.imageclassifier import BoxImageClassifier
from boxes.builtin.learners.trainers import BoxTrainer

from framework.dialog.AlertDialog import AlertDialog

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

        plotter = BoxPlotScatter.Box(self,'Dimension Reducer')
        plotter.move(100, 50)
        self.listBox.append(plotter)

        randomGenerator = BoxRandomGenerator.Box(self,'random generator')
        randomGenerator.move(100,300)
        self.listBox.append(randomGenerator)

        train_image = BoxImageLoader.Box(self,'training-data loader')
        train_image.move(100,600)
        self.listBox.append(train_image)

        validation_image = BoxImageLoader.Box(self,'validation-data loader')
        validation_image.move(500,600)
        self.listBox.append(validation_image)

        model = BoxImageClassifier.Box(self,'Classfication Model')
        model.move(100,800)
        self.listBox.append(model)

        trainer = BoxTrainer.Box(self,'Trainer')
        trainer.move(500,800)
        self.listBox.append(trainer)

        """
        mnist = BoxMNIST.Box(self,[1],[1],'MNIST')
        mnist.move(100,500)
        self.listBox.append(mnist)
        """ 

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

        arrow_style = 'narrow-short'

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

            condition_flag = True
            condition_flag = False if not currBox else condition_flag
            condition_flag = False if not port else condition_flag
            condition_flag = False if currBox == self.selectedBox else condition_flag

            if not self.beginningPort.checkPortMatch(port): 
                condition_flag = False 
                AlertDialog.show(self,'Port types do not match.\nCheck the types')

            if condition_flag:
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
