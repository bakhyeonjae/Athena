import importlib

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from boxes.builtin.visualisers.imageviewer import BoxImageViewer

class BoxLoader:
    @classmethod
    def createBox(self, module_name, class_name, container):
        my_class = getattr(importlib.import_module('{}.{}'.format(module_name,class_name)), 'Box')
        instance = my_class(container,'Name this box')
        return instance

    @classmethod
    def findModuleName(self,baseDir,moduleName):
        path_name = '{}/{}'.format(baseDir,moduleName.replace('.','/'))
        files = list(next(os.walk(path_name))[2])
        module_name = None
        for fname in files:
            if 'Box' in fname and '.py' in fname:
                module_name = fname
        return module_name.replace('.py','')

    @classmethod
    def loadBoxDescription(self,baseDir,moduleName,receiver):
        fname = 'Description.md'
        path_name = '{}/{}'.format(baseDir,moduleName.replace('.','/'))
        full_name = '{}/{}'.format(path_name,fname)
        with open(full_name) as f:
            md_data = f.read()
            receiver.displayBoxDescription(md_data)
