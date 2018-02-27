from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import math
import Port

class CommonModuleBox(QFrame):
    
    def __init__(self, core=None, parent=None, inputPortNum=None, outputPorts=None, instName = '', typeName = ''):
        QFrame.__init__(self, parent)

        self.beingConnected = False
        self.parent = parent
        self.popupActions = []  # list of dictionary, Key :"title","desc","method"
        self.inPorts = []
        self.outPorts = []
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(2)
        self.setStyleSheet("background-color: rgb(230,230,230); border: 1px solid black;")
        self.setContentsMargins(1,1,1,1)
        self.instName = instName
        self.core = core
        self.isOpened = False
        self.beginningPort = None
        self.selectedBox = None

        self.penStart = QPen(QColor(255,0,0))
        self.penStart.setWidth(3)        

        self.penEnd = QPen(QColor(0,0,0))
        self.penEnd.setWidth(1)
        self.brushEnd = QBrush(QColor(0, 0, 0, 255))

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.inputLayout = QHBoxLayout()
        self.inputLayout.addStretch()
        for port_core in inputPortNum:
            new_port = Port.ViewPortIn(self)
            new_port.setPortCore(port_core)
            port_core.setView(new_port)
            self.inPorts.append(new_port)
            self.inputLayout.addWidget(new_port)
            self.inputLayout.addStretch()
        
        self.outputLayout = QHBoxLayout()
        self.outputLayout.addStretch()
        for port_core in outputPorts:
            new_port = Port.ViewPortOut(self)
            new_port.setPortCore(port_core)
            port_core.setView(new_port)
            self.outPorts.append(new_port)
            self.outputLayout.addWidget(new_port)
            self.outputLayout.addStretch()

        self.layout.addLayout(self.outputLayout)
        self.layout.addStretch()
        self.instName = QLabel(instName)
        self.instName.setStyleSheet("border: 0px")
        self.layout.addWidget(self.instName)
        self.typeName = QLabel('(%s)' % typeName)
        self.typeName.setStyleSheet("border: 0px")
        self.layout.addWidget(self.typeName)
        self.layout.addStretch()
        self.layout.addLayout(self.inputLayout)
        
        self.setLayout(self.layout)

        self.resize(self.sizeHint())
        self.show()

        menus = [{"title":"Run", "desc":"Configure module parameters", "method":self.run},
                 {"title":"Delete", "desc":"Configure module parameters", "method":self.deleteBox},
                 {"title":"Step Into", "desc":"Open this box", "method":self.stepIntoBox},
                 {"title":"Step out", "desc":"Open this box", "method":self.stepOutBox},
                 {"title":"Export","desc":"Generate Code", "method":self.export},
                 {"title":"save","desc":"save to file", "method":self.save}
                ]
        self.setPopupActionList(menus)
        self.configPopupMenu()

    def save(self):
        self.core.save('test.box')

    def setOutputPorts(self,ports):
        for port_core in ports:
            new_port = Port.ViewPortOut(self)
            new_port.setPortCore(port_core)
            port_core.setView(new_port)
            self.outPorts.append(new_port)
            self.outputLayout.addWidget(new_port)
            self.outputLayout.addStretch()

    def setInputPorts(self,ports):
        for port_core in ports:
            new_port = Port.ViewPortIn(self)
            new_port.setPortCore(port_core)
            port_core.setView(new_port)
            self.inPorts.append(new_port)
            self.inputLayout.addWidget(new_port)
            self.inputLayout.addStretch()

    def setName(self,name):
        self.instName.setText(name)

    def export(self):
        pass

    def setAsBlackBox(self):
        self.showTitles()
        self.resize(self.sizeHint())
        self.setAcceptDrops(False)

    def stepIntoBox(self):
        self.core.openBox()

    def stepOutBox(self):
        self.core.openParentBox()

    def hideTitles(self):
        """
        Hide texts on Box View when a box is docked on main workspace
        """
        self.isOpened = True
        self.instName.hide()
        self.typeName.hide()
        self.setAcceptDrops(True)

    def showTitles(self):
        self.instName.show()
        self.typeName.show()

    def deleteBox(self):
        # Disconnect all the connections with output port
        for port in self.outPorts:
            port.deleteConnectionLine()
            if port:
                if port.connectedTo:
                    port.connectedTo.disconnectPort()
                port.disconnectPort()

        # Disconnect all the connections with input port
        for port in self.inPorts:  
            # connection instance belongs to output ports.
            if port:
                if port.connectedTo:
                    port.connectedTo.disconnectPort()
                port.disconnectPort()

       	self.parent.deleteBox(self) 

    def configPopupMenu(self):
        pass

    def clearAllHighlightedEdges(self):
        if self.core.boxes:
            for box in self.core.boxes:
                for port in box.inputs:
                    if port.getEdge():
                        port.getEdge().getView().setHighlight(False)
                for port in box.outputs:
                    if port.getEdge():
                        port.getEdge().getView().setHighlight(False)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.core.boxes:
                for box in self.core.boxes:
                    for port in box.inputs:
                        if port.getEdge():
                            if port.getEdge().getView().isOnEdge(event.pos()):
                                self.clearAllHighlightedEdges()
                                port.getEdge().getView().setHighlight(True)
                    for port in box.outputs:
                        if port.getEdge():
                            if port.getEdge().getView().isOnEdge(event.pos()):
                                self.clearAllHighlightedEdges()
                                port.getEdge().getView().setHighlight(True)
            self.update()        
        else:
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
        self.setPopupActionList(menu_list)

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
            if port.getEdge():
                if port.getEdge().getView():
                    port.getEdge().getView().setSrcCoord(QPoint(port.pos().x()+port.width()/2,port.pos().y()+port.height()/2) + self.pos())

        for inport in self.inPorts:
            if inport.getEdge():
                if inport.getEdge().getView():
                    inport.getEdge().getView().setDstCoord(QPoint(inport.pos().x()+inport.width()/2,inport.pos().y()+inport.height()) + inport.parent.pos())

    def run(self):
        self.core.run()

    def execute(self):
        pass

    def propagateExecution(self):
        for port in self.inPorts:
            port.propagateExecution()

    def dragEnterEvent(self, e):
        if not self.isOpened:
            return

        for box in self.core.boxes:
            if box.view.checkPosition(e.pos()):
                self.selectedBox = box.view

        if self.selectedBox:
            port = self.selectedBox.isConnecting(e.pos())
            if port:
                self.beingConnected = True
                self.beginningPort = port
                self.beginningPort.createConnectionLine()
            else:
                self.compensated_pos = e.pos() - self.selectedBox.pos()

        e.accept()

    def dragMoveEvent(self, e):
        if not self.isOpened:
            return

        if self.beingConnected:
            self.beginningPort.updateDstPosition(e.pos())
        else:
            if self.selectedBox:
                position = e.pos()
                self.selectedBox.move(position - self.compensated_pos)
                self.selectedBox.updatePortPos()

        self.update()
        e.accept()

    def dropEvent(self, e):
        if not self.isOpened:
            return

        if self.beingConnected:
            currBox = None
            port = None
            for box in self.core.boxes:
                if box.view.checkPosition(e.pos()):
                    currBox = box.view
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
                edge = self.beginningPort.getEdge()
                edge.connectPorts(self.beginningPort.core,port.core)
            else:
                self.beginningPort.deleteConnectionLine()
   
            self.beingConnected = False
            
        self.selectedBox = None
        self.update()

        e.setDropAction(Qt.MoveAction)
        e.accept()

    def paintEvent(self, eventQPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(self.penStart)        
        qp.setRenderHints(QPainter.Antialiasing, True)
        qp.setPen(self.penEnd)
        qp.setBrush(self.brushEnd)

        if self.beingConnected:
            self.beginningPort.getEdge().getView().drawLine(qp)

        # Scan all the output ports to draw connected lines.
        for box in self.core.boxes:
            for port in box.outputs:
                if port.isConnected():
                    port.getEdge().updateViewPos()
                    port.getEdge().getView().drawLine(qp)

        if self.core.isOpened:
            for port in self.core.inputs:
                if port.isConnected():
                    port.getEdge().updateViewPos()
                    port.getEdge().getView().drawLine(qp)
        qp.end()
