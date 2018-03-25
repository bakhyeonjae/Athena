class CodeNode(object):
    def __init__(self):
        self.boxSpec = None
        self.className = None
        self.instanceID = None
        self.dstNode = None
        self.srcNode = []
        self.paramName = ''
        self.retName = ''

    def setClassName(self,name):
        self.className = name

    def setBoxSpec(self,spec):
        self.boxSpec = spec

    def addSrcNode(self,node):
        self.srcNode.append(node)
        node.setDstNode(self)
    
    def getSrcNodes(self):
        return self.srcNode

    def setDstNode(self,node):
        self.dstNode = node

    def setInstanceID(self,ID):
        self.instanceID = ID

    def setRetName(self,name):
        self.retName = name

    def setParamName(self,name):
        self.paramName = name

    def displayGraph(self):
        self.displayNode()
        self.displayChild()

    def displayChild(self):
        print('')
        for node in self.srcNode:
            node.displayGraph()

    def displayNode(self):
        print('-----------------')
        print('node ref : {}'.format(self))
        print('spec : {}'.format(self.boxSpec))
        print('class : {}'.format(self.className))
        print('ID : {}'.format(self.instanceID))
        print('dst : {}'.format(self.dstNode))
        print('return variable name for extracting value : {}'.format(self.retName))
        print('param variable name for next code block : {}'.format(self.paramName))
        
class ConfigNode(CodeNode):
    def __init__(self):
        super().__init__()
        self.paramValue = ''

    def setParamValue(self, val):
        self.paramValue = val

    def displayNode(self):
        print('--------------------------')
        print('node ref : {}'.format(self))
        print('ID : {}'.format(self.instanceID))
        print('dst : {}'.format(self.dstNode))
        print('param variable name for next code block : {}'.format(self.paramName))
        print('return value : {}'.format(self.paramValue))
