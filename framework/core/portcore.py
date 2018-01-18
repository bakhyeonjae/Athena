class Port(object):
    def __init__(self, box, instName):
        self.dataType = None
        self.box = box
        self.name = instName
        self.connectedTo = None

    def setView(self,viewPort):
        self.view = viewPort

    def isConnected(self):
        if self.connectedTo:
            return True
        else:
            return False

    def disconnectPort(self):
        connectedTo = self.connectedTo
        self.connectedTo = None

        if connectedTo:
            connectedTo.disconnectPort()

class PortIn(Port):
    def __init__(self, box, instName):
        super().__init__(box, instName)
        self.targetType = None # 'code-param' / 'box-port'
        self.targetPort = None
        self.targetClass = None
        self.targetParam = None

    def propagateExecution(self):
        if self.connectedTo:
            self.connectedTo.propagateExecution()

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
        self.connectedTo = portOut

    def getConnection(self):
        if self.connectedTo:
            return self.connectedTo.getConnection()
        else:
            return None

class PortOut(Port):
    def __init__(self, box, instName):
        super().__init__(box, instName)
        self.data = None

    def setView(self,viewPort):
        self.view = viewPort

    def transferData(self, data):
        if self.connectedTo:
            self.data = data   # if it requires caching...  I'm not so sure if it's required or not now. 
            self.connectedTo.passToBox(data)

    def propagateExecution(self):
        self.box.run()

    def connectPort(self,portIn):
        self.connectedTo = portIn
        portIn.connectPort(self)

    def getConnection(self):
        return self.view.getConnection()

