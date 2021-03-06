""" Port module consists of 3 classes.

.. uml::

    @startuml

    'style options 
    skinparam monochrome true
    skinparam circledCharacterRadius 0
    skinparam circledCharacterFontSize 0
    skinparam classAttributeIconSize 0
    hide empty members

    Port <|-- PortIn
    Port <|-- PortOut

    Port : edgeIn
    Port : edgeOut
    Port : connectEdge(edge)
    Port : getEdge()
    Port : setView(view)
    Port : getView()
    Port : isConnected()
    Port : disconnectPort()
    PortOut : transferData(data)
    PortOut : propagateExecution()
    PortOut : getConnection()
    PortIn : targetType
    PortIn : targetPort
    PortIn : targetClass
    PortIn : targetParam
    PortIn : propagateExecution()
    PortIn : configFromDesc(desc)
    PortIn : passToBox(data)
    PortIn : getData()
    PortIn : connectPort(portOut)
    PortIn : getConnection()

    @enduml

"""

from framework.core.codenode import ConfigNode

class Port(object):
    """ Common port interface
    """
    def __init__(self, box, instName):
        self.dataType = None
        self.box = box
        self.name = instName
        self.connectedTo = None
        #self.edge = None
        self.edgeIn = None
        self.edgeOut = None
        self.view = None
        self.exportFlag = False
        self.desc = None

    def setDescription(self,desc):
        self.desc = desc

    def getExportFlag(self):
        return self.exportFlag

    def setExportFlag(self):
        self.exportFlag = True
        self.view.setHighLighted()

    def resetExportFlag(self):
        self.exportFlag = False
        self.view.resetHighLighted()
    
    def isBoxOpened(self):
        """ Check if the box is opened or not

        Returns:
            boolean

            True -- The box is opened on the screen.
            False -- The box is closed.
        """
        return self.box.isOpened

    def connectEdge(self, edge, direction='AUTO'):
        """
        Args:
            edge : (edgecore.Edge)
        """
        if 'IN' == direction:
            self.edgeIn = edge
        elif 'OUT' == direction:
            self.edgeOut = edge
        else:
            if self.isBoxOpened():
                self.edgeIn = edge
            else:
                self.edgeOut = edge
        #self.edge = edge

    def getEdge(self):
        if self.isBoxOpened():
            return self.edgeIn
        else:
            return self.edgeOut
        #return self.edge

    def setView(self,viewPort):
        self.view = viewPort

    def getView(self):
        return self.view

    def isConnected(self):
        if self.isBoxOpened():
            if self.edgeIn:
                return True
            else:
                return False
        else:
            if self.edgeOut:
                return True
            else:
                return False
            
        #if self.edge:
        #    return True
        #else:
        #    return False

    def disconnectPort(self):
        if self.isBoxOpened():
            self.edgeIn = None
        else:
            self.edgeOut = None
        self.edge = None

    def createEdge(self):
        self.box.createEdge(self)
        if self.isBoxOpened():
            return self.edgeIn
        else:
            return self.edgeOut

    def getName(self):
        return self.name

class PortConfig(Port):
    def __init__(self, box, instName, value):  
        super().__init__(box, instName)
        self.targetType = None # 'code-param' / 'box-port'
        self.targetPort = None
        self.targetClass = None
        self.targetParam = None
        self.data = value

    def getData(self):
        return self.data

    def setData(self,val):
        self.data = val

    def propagateExecution(self):
        self.edgeIn.passToBox(float(self.data))  # for only test

    def configFromDesc(self,desc):
        # set target class and parameter name
        target_desc = desc['connect']
        self.targetClass = target_desc.split('@')[1]
        self.targetParam = target_desc.split('@')[0]

    def constructGraph(self,nameParam):
        node = ConfigNode()
        node.setParamName(nameParam)
        node.setParamValue(self.data)
        return node

class PortIn(Port):
    """ PortIn class 
    """
    def __init__(self, box, instName):
        """ Initialise in-port.
        
        Args:
            box: box object that has this port as an element
            instName : instance name of this port
        """
        super().__init__(box, instName)
        self.targetType = None # 'code-param' / 'box-port'
        self.targetPort = None
        self.targetClass = None
        self.targetParam = None

    def constructGraph(self,nameParam):
        graph = None
        if self.edgeOut:
            graph = self.edgeOut.getGraph(nameParam)
        return graph
            
    def setEdge(self,edge):
        """ degree of all the edges is 2. 1 for incoming and 1 for outgoing.

        .. uml::

            @startuml

            PortIn <- BoxCore : connectEdge(edge)
            activate PortIn
            PortIn -> PortIn : isBoxOpened()
            activate PortIn
            PortIn -> BoxCore : isOpened()
            activate BoxCore
            deactivate BoxCore
            deactivate PortIn
            alt opend case
                PortIn -> PortIn : setEdgeIn(edge)
                activate PortIn
                deactivate PortIn
            else closed case
                PortIn -> PortIn : setEdgeOut(edge)
                activate PortIn
                deactivate PortIn
            end
            deactivate PortIn

            @enduml
        """
        pass

    def propagateExecution(self):
        if self.edgeOut:
            self.edgeOut.propagateExecutionToSource()

    def configFromDesc(self,desc):
        """
        {
            "data":"float",
            "type":"batch",
            "name":"variance",
            "connect":"variance@randomgen"
        }
        """
        # set target class and parameter name
        target_desc = desc['connect']
        self.targetClass = target_desc.split('@')[1]
        self.targetParam = target_desc.split('@')[0]

    def isCodeConfigured(self):
        if not self.targetClass:
            return False
        if not self.targetPort:
            return False
        return True

    def passToBox(self,data):
        """
        This method is for PortOut.
        A output port need to transfer data to connected box through input port.
        A output port would call this method to transfer data to a box.
        A box need to get data using getData().
        """
        # Todo : Check the data type.
        if self.box.hasSubBox():
            self.edgeIn.passToBox(data)
        else:
            self.data = data

    def getData(self):
        """
        A box should call this method to get data transferred from connected boxes.
        """
        print('IN PortIn - it\'s box name is ',self.box.name)
        return self.data

    def connectPort(self,portOut):
        self.edge = portOut

    def getConnection(self):
        return self.edge
        
class PortOut(Port):
    def __init__(self, box, instName):
        super().__init__(box, instName)
        self.data = None

    def transferData(self, data):
        if self.edgeOut:
            self.data = data
            self.edgeOut.passToBox(data)
        
    def propagateExecution(self):
        if self.box.hasSubBox():
            self.edgeIn.propagateExecutionToSource()
        else:
            self.box.run()

    def getConnection(self):
        return self.view.getConnection()

    def constructGraph(self,nameParam):
        graph = None

        if self.box.isComposition():
            if self.edgeIn:
                graph = self.edgeIn.getGraph(nameParam)
        else: 
            node = self.box.getCodeSpecNode(nameParam,self)
            igraphs = self.box.requestGraphToInputs()
            for graph in igraphs:
                if graph:
                    node.addSrcNode(graph)
            cgraphs = self.box.requestGraphToConfigs()
            for graph in cgraphs:
                if graph:
                    node.addSrcNode(graph)
            # Check all the inputs
            return node

        # Merge them
        return graph
