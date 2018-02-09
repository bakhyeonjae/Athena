class Port(object):
    def __init__(self, box, instName):
        self.dataType = None
        self.box = box
        self.name = instName
        self.connectedTo = None
        self.edge = None

    def connectEdge(self, edge):
        self.edge = edge

    def getEdge(self):
        return self.edge

    def setView(self,viewPort):
        self.view = viewPort

    def getView(self):
        return self.view

    def isConnected(self):
        if self.edge:
            return True
        else:
            return False

    def disconnectPort(self):
        self.edge = None

class PortIn(Port):
    def __init__(self, box, instName):
        super().__init__(box, instName)
        self.targetType = None # 'code-param' / 'box-port'
        self.targetPort = None
        self.targetClass = None
        self.targetParam = None

    def propagateExecution(self):
        if self.edge:
            self.edge.propagateExecutionToSource()

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

    def setView(self,viewPort):
        self.view = viewPort

    def passToBox(self,data):
        """
        This method is for PortOut.
        A output port need to transfer data to connected box through input port.
        A output port would call this method to transfer data to a box.
        A box need to get data using getData().
        """
        # Todo : Check the data type.
        self.data = data

    def getData(self):
        """
        A box should call this method to get data transferred from connected boxes.
        """
        return self.data

    def connectPort(self,portOut):
        self.edge = portOut

    def getConnection(self):
        return self.edge
        
class PortOut(Port):
    def __init__(self, box, instName):
        super().__init__(box, instName)
        self.data = None

    def setView(self,viewPort):
        self.view = viewPort

    def transferData(self, data):
        if self.edge:
            self.data = data
            self.edge.passToBox(data)
        
    def propagateExecution(self):
        self.box.run()

    def getConnection(self):
        return self.view.getConnection()

