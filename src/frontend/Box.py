from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import math
import Port

from framework.dialog.TextInputDialog import TextInputDialog
from framework.dialog.ConfigDialog import ConfigDialog
from framework.dialog.GlobalConfigDialog import GlobalConfigDialog
from framework.dialog.PortArrayDialog import PortArrayDialog
from framework.dialog.documentdialog import DocumentDialog

class CommonModuleBox(QFrame):
    
    def __init__(self, core=None, parent=None, inputPortNum=None, outputPorts=None, instName = '', typeName = ''):
        QFrame.__init__(self, parent)

        self.beingConnected = False
        self.parent = parent
        self.popupActions = []  # list of dictionary, Key :"title","desc","method"
        self.inPorts = []
        self.outPorts = []
        self.cfgVars = []
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(2)
        self.setStyleSheet("background-color: rgb(230,230,230); border: 1px solid black;")
        self.setContentsMargins(1,1,1,1)
        self.instName = instName
        self.core = core
        self.beginningPort = None
        self.selectedBox = None
        self.flagCoordSaved = False

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
        self.instName.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.instName)
        self.typeName = QLabel('(%s)' % typeName)
        self.typeName.setStyleSheet("border: 0px")
        self.typeName.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.typeName)
        self.layout.addStretch()
        self.layout.addLayout(self.inputLayout)
        
        self.setLayout(self.layout)

        self.resize(self.sizeHint())
        self.show()

    def getX(self):
        return self.x()

    def getY(self):
        return self.y()

    def saveCoordinate(self):
        self.flagCoordSaved = True
        self.posX = self.x()
        self.posY = self.y()
        self.sizeWidth = self.width()
        self.sizeHeight = self.height()

    def restoreCoordinate(self):
        if self.flagCoordSaved:
            self.move(self.posX, self.posY)
            self.resize(self.sizeWidth, self.sizeHeight)
            self.flagCoordSaved = False
        
    def configPopupMenu(self,menuType):
        # Common - Run, Delete, Save, Another Input Port, Another Output Port, Name, Config variables
        menus = [{"title":"Run", "desc":"Configure module parameters", "method":self.run},
                 {"title":"Delete", "desc":"Configure module parameters", "method":self.deleteBox},
                 {"title":"Save","desc":"save to file", "method":self.save},
                 {"title":"Another input port","desc":"Add an input port", "method":self.addInPort},
                 {"title":"Another output port","desc":"Add an output port", "method":self.addOutPort},
                 {"title":"Name","desc":"Give a name to this box", "method":self.rename},
                 {"title":"Config variables","desc":"Configure internal variables", "method":self.configParams},
                 {"title":"Add an Input Port Array","desc":"Add an input port array", "method":self.addInputPortArray},
                 {"title":"Add an Output Port Array","desc":"Add an output port array", "method":self.addOutputPortArray},
                 {"title":"Document","desc":"Document on this box", "method":self.composeDoc}
                ]
        # Composition - Step Into, Step out
        if 'COMPOSITION' == menuType:
            menus.append({"title":"Step Into", "desc":"Open this box", "method":self.stepIntoBox})
            menus.append({"title":"Step out", "desc":"Open this box", "method":self.stepOutBox})
            menus.append({"title":"Config components", "desc":"Open this box", "method":self.configSubBoxParams})

        elif 'CODE' == menuType:
            menus.append({"title":"Open Code", "desc":"Open Code", "method":self.editCode})

        self.setPopupActionList(menus)

    def composeDoc(self):
        self.core.checkDocumentFile()
        composer = self.core.getDocumentComposer()
        desc, inport, outport, cfg, ret = DocumentDialog.getText(composer.getDesc(), composer.getInText(), composer.getOutText(), composer.getConfigText())
        if QDialog.Accepted == ret:
            composer.compose(desc,outport,inport,cfg)

    def addInputPortArray(self):
        name, number, ret = PortArrayDialog.getParameters('Add Input port array')
        if QDialog.Accepted == ret:
            self.core.createPortArray(name,number, 'IN')

    def addOutputPortArray(self):
        name, number, ret = PortArrayDialog.getParameters('Add output port array')
        if QDialog.Accepted == ret:
            self.core.createPortArray(name,number, 'OUT')

    def configSubBoxParams(self):
        params, ret = GlobalConfigDialog().getParameters(params=self.core.getConfigList())
        if QDialog.Accepted == ret:
            self.core.updateComponentConfig(params)

    def setTypeName(self,name):
        self.typeName.setText(name)

    def editCode(self):
        self.core.editCode()

    def addConfigParams(self):
        self.core.addConfigParams()

    def getConfigParams(self):
        self.core.getConfigParams()

    def configParams(self):
        params, ret = ConfigDialog().getParameters(params=self.core.getConfigParams())
        if QDialog.Accepted == ret:
            self.core.setConfigParams(params)

    def rename(self):
        name, ret = TextInputDialog.getText('Give a name to the box')
        self.setName(name)

    def addInPort(self):
        name, ret = TextInputDialog.getText('Name an input port')
        if QDialog.Accepted == ret:
            self.core.addInPort(name)

    def addOutPort(self):
        name, ret = TextInputDialog.getText('Name an output port')
        if QDialog.Accepted == ret:
            self.core.addOutPort(name)

    def save(self):
        self.core.saveBoxPackage()
        self.core.controlTower.localBoxTree.update()

    def keyPressEvent(self, event):
        key = event.key()
        if ord('d') == key or ord('D') == key:
            edge = self.getHighlightedEdge()
            if edge:
                port_src = edge.source
                port_tgt = edge.target
                port_src.disconnectPort()
                port_tgt.disconnectPort()
                self.update()

    def needConfigPorts(self,port):
        if port.getView() in self.cfgVars: 
            return False
        else:
            return True
    
    def setConfigParamPorts(self,ports):
        for port_core in ports:
            if self.needConfigPorts(port_core):
                new_port = Port.ViewPortConfig(self)
                new_port.setPortCore(port_core)
                port_core.setView(new_port)
                self.cfgVars.append(new_port)
        # Put config ports just above input ports
        """
        for port in self.cfgVars:
            y = self.height() - port.height()
            port.move(30,y-10)
            if self.isOpened:
                port.show()
            else:
                port.hide()
        """
        if self.core.isOpened:
            num_var = len(self.cfgVars)
            width = self.width()
            interval = width / num_var
            x = interval / 2
            for port in self.cfgVars:
                y = self.height() - port.height()
                port.move(x,y-30)
                x += interval
                port.show()

    def needOutputPortView(self, port):
        need_flag = True
        for idx in range(self.outputLayout.count()):
            port_view = self.outputLayout.itemAt(idx).widget()
            if port.getView()== port_view and port.getView() and port_view:
                need_flag = False
                break
        return need_flag

    def setOutputPorts(self,ports):
        for port_core in ports:
            if self.needOutputPortView(port_core):
                new_port = Port.ViewPortOut(self)
                new_port.setPortCore(port_core)
                port_core.setView(new_port)
                self.outPorts.append(new_port)
                self.outputLayout.addWidget(new_port)
                self.outputLayout.addStretch()

    def needInputPortView(self, port):
        need_flag = True
        for idx in range(self.inputLayout.count()):
            port_view = self.inputLayout.itemAt(idx).widget()
            if port.getView()== port_view and port.getView() and port_view:
                need_flag = False
                break
        return need_flag

    
    def removePort(self, port):
        if port in self.inPorts:
            idx = self.inPorts.index(port)
            self.inputLayout.removeWidget(port)
            port.setParent(None) 
        if port in self.outPorts:
            idx = self.outPorts.index(port)
            self.outputLayout.removeWidget(port)
            port.setParent(None)

    def setInputPorts(self,ports):
        for port_core in ports:
            if self.needInputPortView(port_core):
                new_port = Port.ViewPortIn(self)
                new_port.setPortCore(port_core)
                port_core.setView(new_port)
                self.inPorts.append(new_port)
                self.inputLayout.addWidget(new_port)
                self.inputLayout.addStretch()

    def setName(self,name):
        self.instName.setText(name)
        self.core.setName(name)

    def getName(self):
        return self.instName.text()

    def export(self):
        self.core.composeCode()

    def setAsBlackBox(self):
        self.showTitles()
        self.resize(self.sizeHint())
        self.setAcceptDrops(False)

    def stepIntoBox(self):
        self.core.openBox()
        num_var = len(self.cfgVars)
        if num_var > 0:
            width = self.width()
            interval = width / num_var
            x = interval / 2
            for port in self.cfgVars:
                y = self.height() - port.height()
                port.move(x,y-30)
                x += interval
                port.show()

    def stepOutBox(self):
        self.core.openParentBox()
        for var in self.cfgVars:
            var.hide()

    def hideTitles(self):
        """
        Hide texts on Box View when a box is docked on main workspace
        """
        self.core.isOpened = True
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

       	self.parent.core.deleteBox(self.core) 

    def getSelectedOne(self,ports):
        for port in ports:
            if port.getEdge():
                if port.getEdge().getView().isHighlighted():
                    return port.getEdge()

    def getHighlightedEdge(self):
        if self.core.boxes:
            for box in self.core.boxes:
                ret = self.getSelectedOne(box.inputs)
                if ret:
                    return ret
                ret = self.getSelectedOne(box.outputs)
                if ret:
                    return ret
        ret = self.getSelectedOne(self.cfgVars)
        if ret:
            return ret
        ret = self.getSelectedOne(self.inPorts)
        if ret:
            return ret
        ret = self.getSelectedOne(self.outPorts)
        if ret:
            return ret

    def clearEdges(self,ports):
        for port in ports:
            if port.getEdge():
                port.getEdge().getView().setHighlight(False)

    def clearAllHighlightedEdges(self):
        if self.core.boxes:
            for box in self.core.boxes:
                self.clearEdges(box.inputs)
                self.clearEdges(box.outputs)
        self.clearEdges(self.cfgVars)
        self.clearEdges(self.inPorts)
        self.clearEdges(self.outPorts)

    def selectOneEdge(self, ports, event):
        for port in ports:
            if port.getEdge():
                if port.getEdge().getView().isOnEdge(event.pos()):
                    self.clearAllHighlightedEdges()
                    port.getEdge().getView().setHighlight(True)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.core.boxes:
                for box in self.core.boxes:
                    self.selectOneEdge(box.inputs,event)
                    self.selectOneEdge(box.outputs,event)
            self.selectOneEdge(self.cfgVars,event)
            self.selectOneEdge(self.inPorts,event)
            self.selectOneEdge(self.outPorts,event)
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
        menu = None

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

    def isConnecting(self, pos, beginFrom='OUTPORT'):
        if 'OUTPORT' == beginFrom:
            for port in self.outPorts:
                if port.checkPosition(pos-self.pos()):
                    return port
        elif 'INPORT' == beginFrom:
            for port in self.inPorts:
                if port.checkPosition(pos):
                    return port
        elif 'CONFIG' == beginFrom:
            for port in self.cfgVars:
                if port.checkPosition(pos):
                    return port
        return None

    def isArrived(self, pos, arriveAt='INPORT'):
        if 'INPORT' == arriveAt:
            for port in self.inPorts:
                if port.checkPosition(pos-self.pos()):
                    return port
        elif 'OUTPORT' == arriveAt:
            for port in self.outPorts:
                if port.checkPosition(pos):
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
        if not self.core.isOpened:
            return

        for box in self.core.boxes:
            if box.view.checkPosition(e.pos()):
                self.selectedBox = box.view

        if self.selectedBox:
            port = self.selectedBox.isConnecting(e.pos(),beginFrom='OUTPORT')
            if port:
                self.beingConnected = True
                self.beginningPort = port
                self.beginningPort.createConnectionLine()
            else:
                self.compensated_pos = e.pos() - self.selectedBox.pos()
        else:
            in_port = self.isConnecting(e.pos(),beginFrom='INPORT')
            cfg_port =self.isConnecting(e.pos(),beginFrom='CONFIG')
            if in_port or cfg_port:
                self.beingConnected = True
                self.beginningPort = in_port if in_port else cfg_port
                self.beginningPort.createConnectionLine()
            else:
                self.compensated_pos = e.pos() - self.pos()

        e.accept()

    def dragMoveEvent(self, e):
        if not self.core.isOpened:
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
        if not self.core.isOpened:
            return

        if self.beingConnected:
            currBox = None
            port = None
            for box in self.core.boxes:
                if box.view.checkPosition(e.pos()):
                    currBox = box.view

            if not currBox:
                if self.checkPosition(e.pos()):
                    currBox = self

            if currBox:
                if currBox == self:
                    port = currBox.isArrived(e.pos(), arriveAt='OUTPORT')
                else:
                    port = currBox.isArrived(e.pos(), arriveAt='INPORT')

            condition_flag = True
            condition_flag = False if not currBox else condition_flag
            condition_flag = False if not port else condition_flag
            condition_flag = False if currBox == self.selectedBox else condition_flag

            if port:
                if not self.beginningPort.checkPortMatch(port): 
                    condition_flag = False 
                    AlertDialog.show(self,'Port types do not match.\nCheck the types')
            else:
                condition_flag = False

            if condition_flag:
                edge = self.beginningPort.getEdge()
                edge.connectPorts(self.beginningPort.core,port.core)
            else:
                #self.beginningPort.deleteConnectionLine()
                self.beginningPort.disconnectPort()
   
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
        if self.core.isOpened:
            for box in self.core.boxes:
                for port in box.outputs:
                    if port.isConnected():
                        port.getEdge().updateViewPos()
                        port.getEdge().getView().drawLine(qp)

            for port in self.core.inputs:
                if port.isConnected():
                    port.getEdge().updateViewPos()
                    port.getEdge().getView().drawLine(qp)

            for port in self.core.cfgVars:
                if port.isConnected():
                    port.getEdge().updateViewPos()
                    port.getEdge().getView().drawLine(qp)
        qp.end()
