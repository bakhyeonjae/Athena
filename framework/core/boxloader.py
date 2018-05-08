import importlib
import json

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.append(currentdir)
sys.path.append(parentdir)

from src.frontend.Box import CommonModuleBox
from framework.core import boxcore
from systemconfig import SystemConfig

class BoxLoader(object):
    @classmethod
    def createBox(cls, module_name, class_name, ancestor, controlTower):
        print('module_name : {}, class_name : {}'.format(module_name,class_name))
        repo_indicator = module_name.split('/')[0] 
        if 'global' == repo_indicator:
            file_name = '{}/{}/{}'.format(SystemConfig.getRepository(),module_name,class_name)
        elif 'workspace' == repo_indicator:
            file_name = '{}/{}/{}'.format(SystemConfig.getRepository(),module_name,class_name)
        else:
            file_name = '{}/{}/{}'.format(SystemConfig.getLocalWorkSpaceDir(),module_name,class_name)

        boxes = []
        spec_name = '{}/{}'.format(module_name,class_name)
        print('file_name in createBox is {}'.format(file_name))
        with open(file_name,'r') as f:
            data = f.read()
            desc = json.loads(data)
            print('createBox : {}'.format(spec_name))
            box = boxcore.Box(desc,ancestor,spec_name.replace('../','').replace('/','.').replace('.box',''),controlTower)
        return box

    @classmethod
    def findModuleName(cls,baseDir,moduleName):
        path_name = '{}/{}'.format(baseDir,moduleName.replace('.','/'))
        files = list(next(os.walk(path_name))[2])
        module_name = None
        for fname in files:
            if '.box' in fname:
                module_name = fname
        return module_name

    @classmethod
    def loadBoxDescription(cls,baseDir,moduleName,receiver):
        fname = 'Description.md'
        path_name = '{}/{}'.format(baseDir,moduleName.replace('.','/'))
        full_name = '{}/{}'.format(path_name,fname)
        with open(full_name) as f:
            md_data = f.read()
            receiver.displayBoxDescription(md_data)

    @classmethod
    def findModuleNameByBoxID(cls,boxID):
        """
        Find module name by box ID

        :param boxID:

        :rtype: list of strings
        """
        version = boxID.split('@')[1]
        box_dir = '{}/{}'.format(SystemConfig.getBoxDir(),boxID.split('@')[0].replace('.','/'))
        return box_dir

    @classmethod
    def getModuleName(cls,currItem):
        if currItem:
            name = currItem.text(0)
            return '{}/{}'.format(cls.getModuleName(currItem.parent()),name).lstrip('/')
        else:
            return ''

