from PySide.QtGui import *
from PySide.QtCore import *
import sys

class CommonModuleBox(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setStyleSheet("QLabel { background-color : white; color : black; border: 20px solid white}")

    def mouseReleaseEvent(self, event):
        #print 'Label clicked!'
        pass

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData(self)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)


class TrainerBox(CommonModuleBox):
    def __init__(self, parent=None):
        CommonModuleBox.__init__(self, parent)
        self.setText('CNN Trainer')

class ModelBox(CommonModuleBox):
    def __init__(self, parent=None):
        CommonModuleBox.__init__(self, parent)
        self.setText('CNN Model')

class TesterBox(CommonModuleBox):
    def __init__(self, parent=None):
        CommonModuleBox.__init__(self, parent)
        self.setText('CNN Tester')

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.trainer= TrainerBox(self)
        self.trainer.move(100, 50)

        self.model= ModelBox(self)
        self.model.move(100, 200)

        self.tester = TesterBox(self)
        self.tester.move(100, 350)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 550)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.button.move(position)
        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywin = MainWindow()
    mywin.show()
    sys.exit(app.exec_())
