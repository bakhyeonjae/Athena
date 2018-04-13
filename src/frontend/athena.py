from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys
import math
import os

from Box import CommonModuleBox
from infoview import InfoView
from mainwnd import MainWnd

sys.path.append("..")
sys.path.append("../..")

from framework.dialog.AlertDialog import AlertDialog
from framework.core.boxloader import BoxLoader
from controltower.controltower import ControlTower

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
        self.openedBox.setFocus()

    def deleteBox(self, box):
        selected = next(x for x in self.listBox if x == box)
        selected.setParent(None)
        self.listBox.remove(selected)
        del selected
        self.update()
        
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
    mainWnd = MainWnd()
    mywin = TopWindow()
    controlTower = ControlTower()
    controlTower.setWorkSpace(mywin.frame)
    controlTower.setInfoWindow(mywin.viewInfo)
    controlTower.setBoxTree(mywin.tree)
    controlTower.constructInitState()
    mainWnd.setCentralWidget(mywin)
    mainWnd.show()
    sys.exit(app.exec_())
