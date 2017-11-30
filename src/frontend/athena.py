from PySide.QtGui import *
from PySide.QtCore import *
import sys
#import trainerbox
import trainerboxcnn

class CommonModuleBox(QLabel):
    popupActions = [];  # list of dictionary, Key :"title","desc","method"

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setStyleSheet("QLabel { background-color : white; color : black; border: 20px solid white}")

    def mouseReleaseEvent(self, event):
        self.createPopupActions()
        self.createPopupMenu()

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData(self)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)

    def createPopupActions(self):
        menu_list = []
        setPopupActionList(menu_list)

    def createPopupMenu(self):
        """ This method creates popup menu and display on screen. Menu items will be given by child classes. Child classes must override createPopupActions to set menu items.
        """
        menu = QMenu()

        for action in self.popupActions:
            act = QAction(action["title"], self)
            act.setStatusTip(action["desc"])
            act.triggered.connect(action["method"])
            menu.addAction(act)

        menu.exec_(QCursor.pos())

    def setPopupActionList(self,menuList):
        for menu in menuList:
            if menu not in self.popupActions:
                self.popupActions.append(menu) 

    def checkPosition(self,pos):
        if pos.x() < self.pos().x():
            return False
        if pos.x() > self.pos().x() + self.width():
            return False
        if pos.y() < self.pos().y():
            return False
        if pos.y() > self.pos().y() + self.height():
            return False

        return True

class ModelBox(CommonModuleBox):
    def __init__(self, parent=None):
        CommonModuleBox.__init__(self, parent)
        self.setText('CNN Model')

class TesterBox(CommonModuleBox):
    def __init__(self, parent=None):
        CommonModuleBox.__init__(self, parent)
        self.setText('CNN Tester')

class OptimizerBox(CommonModuleBox):
    def __init__(self, parent=None):
        CommonModuleBox.__init__(self, parent)
        self.setText('CNN Optimizer')

class MainWindow(QWidget):
    listBox = []
    selectedBox = None
    compensated_pos = 0

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        trainer= trainerboxcnn.TrainerBoxCNN(self)
        trainer.move(100, 50)
        self.listBox.append(trainer)

        model= ModelBox(self)
        model.move(100, 200)
        self.listBox.append(model)

        tester = TesterBox(self)
        tester.move(100, 350)
        self.listBox.append(tester)

        optimizer = OptimizerBox(self)
        optimizer.move(100, 500)
        self.listBox.append(optimizer)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 700)

    def dragEnterEvent(self, e):
        for box in self.listBox:
            if box.checkPosition(e.pos()):
                self.selectedBox = box
        self.compensated_pos = e.pos() - self.selectedBox.pos()
        e.accept()

    def dragMoveEvent(self, e):
        position = e.pos()
        self.selectedBox.move(position - self.compensated_pos)
        e.accept()

    def dropEvent(self, e):
        self.selectedBox = None
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
