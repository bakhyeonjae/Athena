class CodeGenerator(object):
    def __init__(self,path):
        self.pathName = path

    def exportCode(self, targetPort, orderedNodes):
        self.genImports(orderedNodes)
        self.genCode(orderedNodes)
        self.genSkeleton(targetPort, orderedNodes[-1].getRetVarName())

        with open(self.pathName, 'w', encoding='utf-8') as of:
            of.write(self.importStatements)
            of.write(self.codeBlock)

    def genImports(self, nodes):
        self.importStatements = ''
        for node in nodes:
            self.importStatements += node.getImportStatement()
        self.importStatements += '\n'

    def genCode(self, nodes):
        self.exprs = ''
        for node in nodes:
            self.exprs += node.getInstStatement()
            self.exprs += node.getExecStatement()
            self.exprs += node.getRetVarStatement()
            self.exprs += '\n'

    def genSkeleton(self, port, retvar):
        func_name = '{}_{}'.format(port.box.name, port.name)
        func_name = func_name.replace(' ','')
        self.codeBlock = 'def {}():\n'.format(func_name)
        self.codeBlock += self.exprs
        self.codeBlock += '    return {}\n'.format(retvar)
