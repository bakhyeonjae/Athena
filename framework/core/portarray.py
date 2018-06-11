class PortArray(object):
    def __init__(self, portContainer, n, number, portType):
        self.name = n
        self.number = number
        self.ports = []
        self.container = portContainer
        self.portType = portType

    def updatePort(self):
        for idx in range(self.number):
            port_name = '{}{}'.format(self.name,idx)
            if 'IN' in self.portType:
                self.container.addInPort(port_name)
            elif 'OUT' in self.portType:
                self.container.addOutPort(port_name)
        

