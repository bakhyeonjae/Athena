from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import math
import os

from Box import CommonModuleBox
from infoview import InfoView

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

    def deleteBox(self, box):
        selected = next(x for x in self.listBox if x == box)
        selected.setParent(None)
        self.listBox.remove(selected)
        del selected
        self.update()
    
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

        self.sampleHtml = '''
        <html>
            <body>
            Hello! <br>
            <h1>Nice to meet you</h1>
            </body>
        </html>
        '''
        self.viewInfo = InfoView(self.sampleHtml)
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
