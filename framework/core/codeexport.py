import os, errno
import shutil

from framework.core.systemconfig import SystemConfig

class CodeGenerator(object):
    boxCodeDir = 'libs'
    def __init__(self,path):
        self.pathName = path

    def exportCode(self, targetPort, orderedNodes, fileName):
        self.genImports(orderedNodes)
        self.genCode(orderedNodes)
        name = self.genSkeleton(targetPort, orderedNodes[-1].getRetVarName())
        func_name = '{}'.format(name)

        path_file_name = '{}/{}'.format(self.pathName,fileName)
        with open(path_file_name, 'w', encoding='utf-8') as of:
            of.write(self.importStatements)
            of.write(self.codeBlock)
        return func_name

    def transferLibFiles(self, orderedNodes, targetDir):
        for node in orderedNodes:
            if node.getCodeFile():
                full_src_name = '{}/{}'.format(SystemConfig.getToolDir(),node.getCodeFile())
                target_dir_name = '{}/{}'.format(targetDir,CodeGenerator.boxCodeDir)
                shutil.copy(full_src_name,target_dir_name)
            #print('file : {} --> {}'.format(full_src_name,'{}/{}'.format(targetDir,CodeGenerator.boxCodeDir)))

    def genImports(self, nodes):
        self.importStatements = ''
        for node in nodes:
            self.importStatements += node.getImportStatement(CodeGenerator.boxCodeDir)
        self.importStatements += '\n'

    def genCode(self, nodes):
        self.exprs = ''
        for node in nodes:
            self.exprs += node.getInstStatement()
            self.exprs += node.getExecStatement()
            self.exprs += node.getRetVarStatement()
            self.exprs += '\n'

    def genSkeleton(self, port, retvar):
        """
        return : function_name
        """
        func_name = '{}_{}'.format(port.box.name, port.name)
        func_name = func_name.replace(' ','')
        self.codeBlock = 'def {}():\n'.format(func_name)
        self.codeBlock += self.exprs
        self.codeBlock += '    return {}\n'.format(retvar)
        return func_name

    @classmethod
    def createDir(cls,dirName):
        if not os.path.exists(dirName):
            try: os.makedirs(dirName)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            lib_name = '{}/{}'.format(dirName,cls.boxCodeDir)
            try: os.makedirs(lib_name)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    def exportExampleModule(self, func_name, module_name):
        path_file_name = '{}/{}'.format(self.pathName,'main.py')
        with open(path_file_name, 'w', encoding='utf-8') as of:
            for idx, name in enumerate(module_name): of.write('from {} import {}\n'.format(name.replace('.py',''),func_name[idx]))
            of.write('\n')
            for name in func_name: of.write('{}()\n'.format(name))
