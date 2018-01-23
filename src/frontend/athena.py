from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys
import math
import os

from Box import CommonModuleBox
from infoview import InfoView

#import os,sys,inspect
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#parentdir = os.path.dirname(parentdir)
#sys.path.insert(0,parentdir) 

sys.path.append("..")
sys.path.append("../..")

from boxes.builtin.visualisers.plotscatter import BoxPlotScatter
from boxes.builtin.primitives.genrandom import BoxRandomGenerator
from boxes.builtin.learners.tmpmnist import BoxMNIST
from boxes.builtin.loaders.image import BoxImageLoader
from boxes.builtin.learners.models.imageclassifier import BoxImageClassifier
from boxes.builtin.learners.trainers import BoxTrainer
from boxes.builtin.visualisers.plottimeline import BoxPlotTimeline
from boxes.builtin.visualisers.plotcrossvalidation import BoxPlotCrossValidation
from boxes.builtin.visualisers.imageviewer import BoxImageViewer

from framework.dialog.AlertDialog import AlertDialog
from framework.core.boxloader import BoxLoader
from controltower.controltower import ControlTower

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
        super().__init__()
        self.initUI()

    def setControlTower(self, ct):
        self.controlTower = ct

    def initUI(self):
        self.setAcceptDrops(True)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 580, 700)

        self.penStart = QPen(QColor(255,0,0))
        self.penStart.setWidth(3)        

        self.penEnd = QPen(QColor(0,0,0))
        self.penEnd.setWidth(1)
        self.brushEnd = QBrush(QColor(0, 0, 0, 255))

    def resizeEvent(self, event):
        margin = 10
        width = self.size().width()
        height = self.size().height()
        self.controlTower.openedBox.view.resize(width-margin*2,height-margin*2)

    def dockBox(self, box):
        #register the given box as a main box
        margin = 10
        self.openedBox = box
        width = self.size().width()
        height = self.size().height()

        self.openedBox.move(margin,margin)
        self.openedBox.resize(width-margin*2,height-margin*2)
        self.openedBox.hideTitles()

    #def addBox(self, box):
    #    self.listBox.append(box)
    #    self.dockBox(box)

    def deleteBox(self, box):
        selected = next(x for x in self.listBox if x == box)
        selected.setParent(None)
        self.listBox.remove(selected)
        del selected
        self.update()

    """
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
    """
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
        """
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
        """

    def dragMoveEvent(self, e):
        """
        if self.isConnecting:
            self.beginningPort.updateDstPosition(e.pos())
        else:
            position = e.pos()
            self.selectedBox.move(position - self.compensated_pos)
            self.selectedBox.updatePortPos()

        self.update()
        e.accept()
        """

    def dropEvent(self, e):
        """
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
        """

# left Tree class
class TreeWidget(QTreeWidget):

    def __init__(self,canvas,infoView):

        QTreeWidget.__init__(self)

        self.canvas = canvas
        self.infoView = infoView

        box_dir = '../../boxes'
        categories = self.getSubDir(box_dir)

        self.header = QTreeWidgetItem(["Boxes"])
        self.setHeaderItem(self.header)

        self.constructSubTree(box_dir,self)

        self.itemDoubleClicked.connect(lambda:self.controlTower.createBoxFromDesc(self.currentItem()))
        #self.itemDoubleClicked.connect(lambda: self.canvas.addBox(BoxLoader.createBox('../../boxes{}'.format(self.getModuleName(self.currentItem())),BoxLoader.findModuleName(box_dir,self.getModuleName(self.currentItem())),self.canvas).view))
        #self.itemClicked.connect(lambda: BoxLoader.loadBoxDescription(box_dir,self.getModuleName(self.currentItem()),self.infoView))

    def setControlTower(self, ct):
        self.controlTower = ct

    def constructSubTree(self,pathName,parentItem):
        subitem = self.getSubDir(pathName)
        for category in subitem:
            if '__pycache__' in category:
                continue
            subWidgetItem = QTreeWidgetItem(parentItem, [category])
            self.constructSubTree('{}/{}'.format(pathName,category),subWidgetItem)

    def getSubDir(self,pathName):
        sub_dir = list(list(next(os.walk(pathName))[1]))
        return sub_dir

    def printer(self, treeItem):
        foldername = treeItem.text(0)
        print(foldername + ' selected!!!')
        print(treeItem.parent().text(0))

    def getModuleName(self,currItem):
        if currItem:
            name = currItem.text(0)
            return '{}/{}'.format(self.getModuleName(currItem.parent()),name)
        else:
            return ''

# Top main window has tree and right frame
class TopWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(100, 100, 1600, 900)

        self.frame = MainWindow()
        self.frame.setStyleSheet("background-color: rgb(100, 155, 255)")

        self.viewInfo = InfoView()
        self.viewInfo.setFixedWidth(280)

        self.tree = TreeWidget(self.frame,self.viewInfo)
        self.tree.setFixedWidth(280)
        self.tree.setStyleSheet("background-color: rgb(200, 255, 255)")


        layout = QHBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.frame)
        layout.addWidget(self.viewInfo)
        self.setLayout(layout)

if __name__ == "__main__":
    # check if QApplication already exists
    app = QApplication.instance()
    if not app:     # create QApplication if it doesnt exist
        app = QApplication(sys.argv)
    mywin = TopWindow()
    controlTower = ControlTower()
    controlTower.setWorkSpace(mywin.frame)
    controlTower.setInfoWindow(mywin.viewInfo)
    controlTower.setBoxTree(mywin.tree)
    controlTower.constructInitState()
    mywin.show()
    sys.exit(app.exec_())
