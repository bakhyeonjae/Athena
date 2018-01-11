import importlib
import json

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from boxes.builtin.visualisers.imageviewer import BoxImageViewer
from src.frontend.Box import CommonModuleBox

class BoxLoader:
    @classmethod
    def createBox(self, module_name, class_name, container):
        boxes = []
        with open('{}/{}'.format(module_name,class_name),'r') as f:
            data = f.read()
            desc = json.loads(data)
            box = desc['box']
            subboxes = box['sub-box']
            inputs   = box['in-port']
            outputs  = box['out-port']

            for subbox in box['sub-box']:
                boxes.append(CommonModuleBox(container,len(subbox['in-port']),len(subbox['out-port']),subbox['name'],subbox['type']))

        return boxes

    @classmethod
    def findModuleName(self,baseDir,moduleName):
        path_name = '{}/{}'.format(baseDir,moduleName.replace('.','/'))
        files = list(next(os.walk(path_name))[2])
        module_name = None
        for fname in files:
            #if 'Box' in fname and '.py' in fname:
            if '.box' in fname:
                module_name = fname
        return module_name

    @classmethod
    def loadBoxDescription(self,baseDir,moduleName,receiver):
        fname = 'Description.md'
        path_name = '{}/{}'.format(baseDir,moduleName.replace('.','/'))
        full_name = '{}/{}'.format(path_name,fname)
        with open(full_name) as f:
            md_data = f.read()
            receiver.displayBoxDescription(md_data)
