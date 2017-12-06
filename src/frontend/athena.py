from PySide.QtGui import *
from PySide.QtCore import *
import sys
#import trainerbox
import trainerboxcnn
import Port

#class CommonModuleBox(QLabel):
class CommonModuleBox(QFrame):
    popupActions = []  # list of dictionary, Key :"title","desc","method"
    inPorts = []
    outPorts = []

    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = '', typeName = ''):
        QFrame.__init__(self, parent)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setContentsMargins(1,1,1,1)
        layout = QVBoxLayout()
        inputLayout = QHBoxLayout()
        inputLayout.addStretch()
        for pin in inputPort:
            new_port = Port.PortIn(self)
            self.inPorts.append(new_port)
            inputLayout.addWidget(new_port)
            inputLayout.addStretch()

        bodyLayout = QHBoxLayout()
        bodyLayout.addWidget(QLabel(instName))
        
        outputLayout = QHBoxLayout()
        outputLayout.addStretch()
        for pout in outputPort:
            new_port = Port.PortOut(self)
            self.outPorts.append(new_port)
            outputLayout.addWidget(new_port)
            outputLayout.addStretch()

        layout.addLayout(outputLayout)
        layout.addWidget(QLabel(instName))
        layout.addWidget(QLabel('(%s)' % typeName))
        layout.addLayout(inputLayout)
        
        self.setLayout(layout)
        self.show()

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

    def isConnecting(self,pos):
        for port in self.outPorts:
            if port.checkPosition(pos-self.pos()):
                return port
        return None

    def isArrived(self,pos):
        for port in self.inPorts:
            if port.checkPosition(pos-self.pos()):
                return port
        return None

    def updatePortPos(self):
        for port in self.outPorts:
            print(port)
            if port.getConnection():
                port.getConnection().setSrcCoord(QPoint(port.pos().x()+port.width()/2,port.pos().y()+port.height()/2) + self.pos())

        print("****")
        #for inport in self.inPorts:
        #    if inport.getConnection():
        #        inport.getConnection().setDstCoord(inport.parent.pos())# + QPoint(inport.pos().x()+inport.width()/2,inport.pos().y()+inport.height()/2) + inport.parent.pos())

class ModelBox(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = '', typeName = ''):
        CommonModuleBox.__init__(self, parent, inputPort, outputPort, instName, typeName)

class TesterBox(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = '', typeName = ''):
        CommonModuleBox.__init__(self, parent, inputPort, outputPort, instName, typeName)

class OptimizerBox(CommonModuleBox):
    def __init__(self, parent=None, inputPort = [], outputPort = [], instName = '', typeName = ''):
        CommonModuleBox.__init__(self, parent, inputPort, outputPort, instName, typeName)

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

        trainer= ModelBox(self,[1],[],'Dimension Reducer','Visualiser.tSNE')
        trainer.move(100, 50)
        self.listBox.append(trainer)

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

    def paintEvent(self, eventQPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHints(QPainter.Antialiasing, True)
        if self.isConnecting:
            qp.drawLine(self.beginningPort.getConnection().getSrcCoord(),self.beginningPort.getConnection().getDstCoord())

        # Scan all the output ports to draw connected lines.
        for box in self.listBox:
            for port in box.outPorts:
                if port.isConnected():
                    qp.drawLine(port.getConnection().getSrcCoord(),port.getConnection().getDstCoord())
        qp.end()

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
