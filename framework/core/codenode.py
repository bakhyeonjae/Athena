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

    def getCodeDir(self):
        module_name = self.boxSpec
        if module_name:
            related_dir = module_name.replace('.','/')
            return related_dir
        else:
            return None

    def getCodeFile(self):
        module_name = self.boxSpec
        if module_name:
            file_name = module_name.replace('.','/')
            return '{}.py'.format(file_name)
        else:
            return None
    
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

    def getInstStatement(self):
        return '    {} = {}()\n'.format(self.getInstName(),self.className)

    def getInstName(self):
        return 'inst{}_{}'.format(id(self),self.className)

    def getRetVarStatement(self):
        return '    {} = {}.{}\n'.format(self.getRetVarName(),self.getInstName(),self.retName)

    def getExecStatement(self):
        exec_str = '    {}.execute('.format(self.getInstName())
        for param in self.srcNode:
            if param == self.srcNode[-1]:
                exec_str += '{}={}'.format(param.paramName,param.getRetVarName())
            else:
                exec_str += '{}={},'.format(param.paramName,param.getRetVarName())
        exec_str += ')\n'
        return exec_str

    def getImportStatement(self,directory):
        if self.boxSpec:
            spec_ = self.boxSpec
            module_name = spec_.split('.')[-1]
            return 'from {}.{} import {}\n'.format(directory,module_name,self.className)
        else:
            return ''

    def getRetVarName(self):
        return 'var{}_{}'.format(id(self),self.retName)
        
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

    def getInstStatement(self):
        return ''

    def getExecStatement(self):
        return ''

    def getRetVarStatement(self):
        return '    {} = {}\n'.format(self.getRetVarName(),self.paramValue)
