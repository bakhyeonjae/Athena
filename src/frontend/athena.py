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
from framework.core.systemconfig import SystemConfig
from framework.core.syncbox import SyncBox

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
        
# left Tree class
class TreeWidget(QTreeWidget):

    def __init__(self,canvas,infoView,boxDir,title):

        QTreeWidget.__init__(self)

        self.canvas = canvas
        self.infoView = infoView
        self.boxDir = boxDir

        #box_dir = '../../boxes'
        categories = self.getSubDir(self.boxDir)

        self.header = QTreeWidgetItem([title])
        self.setHeaderItem(self.header)

        self.constructSubTree(self.boxDir,self)

        self.itemDoubleClicked.connect(lambda:self.controlTower.createBoxFromDesc(self.currentItem(),self.boxDir))
        self.itemClicked.connect(lambda:self.controlTower.displayBoxDescription(self.currentItem(),self.boxDir))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.createPopupMenu()
        QTreeWidget.mouseReleaseEvent(self,event)

    def moveToRepo(self):
        synchroniser = SyncBox(controlTower.resource)
        synchroniser.moveBoxToRepo(BoxLoader.getModuleName(self.currentItem()))

    def createPopupMenu(self):
        menu = QMenu()
        act = QAction('Move to cloud workspace', self)
        act.triggered.connect(self.moveToRepo)
        menu.addAction(act)

        menu.exec_(QCursor.pos())
        menu = None

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

    def update(self):
        self.clear()
        self.constructSubTree(self.boxDir,self)

# Top main window has tree and right frame
class TopWindow(QWidget):
    def __init__(self, resource, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(100, 100, 1600, 900)

        self.frame = MainWindow()
        self.frame.setStyleSheet("background-color: rgb(100, 155, 255)")

        self.viewInfo = InfoView()
        self.viewInfo.setFixedWidth(280)
        sample_html = '''
        <html>
            <body>
            Hello!
            </body>
        </html>
        '''
        self.viewInfo.setHtml(sample_html)

        if not resource.checkBoxDirConfigured():
            dirDlg = QFileDialog()
            dirDlg.setFileMode(QFileDialog.Directory)
            if dirDlg.exec_():
                local_box_dir = dirDlg.selectedFiles()
                resource.updateConfigFile(local_box_dir[0])

        
        self.tree = TreeWidget(self.frame,self.viewInfo,resource.getWorkspaceDir(),'Cloud Workspace')
        self.tree.setFixedWidth(280)
        self.tree.setStyleSheet("background-color: rgb(200, 255, 255)")

        self.boxRepoLocal = TreeWidget(self.frame,self.viewInfo,resource.getLocalWorkSpaceDir(),'Local Workspace')
        self.boxRepoLocal.setFixedWidth(280)
        self.boxRepoLocal.setStyleSheet("background-color: rgb(200, 255, 255)")
        self.boxRepoLocal.update()

        layout = QHBoxLayout()
        treeLayout = QVBoxLayout()
        treeLayout.addWidget(self.tree)
        treeLayout.addWidget(self.boxRepoLocal)
        layout.addLayout(treeLayout)
        layout.addWidget(self.frame)
        layout.addWidget(self.viewInfo)
        self.setLayout(layout)

if __name__ == "__main__":
    # check if QApplication already exists
    app = QApplication.instance()
    if not app:     # create QApplication if it doesnt exist
        app = QApplication(sys.argv)
    controlTower = ControlTower()
    mainWnd = MainWnd()
    mywin = TopWindow(controlTower.resource)
    controlTower.setWorkSpace(mywin.frame)
    controlTower.setInfoWindow(mywin.viewInfo)
    controlTower.setBoxTree(mywin.tree)
    controlTower.setLocalBoxTree(mywin.boxRepoLocal)
    controlTower.constructInitState()
    mainWnd.setCentralWidget(mywin)
    mainWnd.setControlTower(controlTower)
    mainWnd.show()
    sys.exit(app.exec_())
