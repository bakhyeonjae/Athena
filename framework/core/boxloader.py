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
        """
        module_name : module name located at 'local dir' / 'server-private' / 'server-global'
        """
        repo_indicator = module_name.split('/')[0] 
        if 'global' == repo_indicator:
            file_name = '{}/{}/{}'.format(controlTower.resource.getWorkspaceDir(),module_name,class_name)
        elif 'workspace' == repo_indicator:
            file_name = '{}/{}/{}'.format(controlTower.resource.getWorkspaceDir(),module_name,class_name)
        else:
            file_name = '{}/{}/{}'.format(controlTower.resource.getLocalWorkSpaceDir(),module_name,class_name)

        boxes = []
        spec_name = '{}/{}'.format(module_name,class_name)

        if os.path.isdir('{}/{}'.format(controlTower.resource.getLocalWorkSpaceDir(),module_name)):
            boxspec_file_name = '{}/{}'.format(controlTower.resource.getLocalWorkSpaceDir(),spec_name)
        elif os.path.isdir('{}/{}'.format(controlTower.resource.getWorkspaceDir(),module_name)):
            boxspec_file_name = '{}/{}'.format(controlTower.resource.getWorkspaceDir(),spec_name)
        
        with open(boxspec_file_name,'r') as f:
            data = f.read()
            desc = json.loads(data)
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
        with open(full_name,'r') as f:
            md_data = f.read()
            receiver.displayBoxDescription(md_data)

    @classmethod
    def findModuleNameByBoxID(cls,boxID,resource):
        """
        Find module name by box ID

        :param boxID:

        :rtype: list of strings
        """
        version = boxID.split('@')[1]
        box_dir = '{}/{}'.format(resource.getWorkspaceDir(),boxID.split('@')[0].replace('.','/'))
        return box_dir

    @classmethod
    def getModuleName(cls,currItem):
        if currItem:
            name = currItem.text(0).replace('.','_')
            return '{}/{}'.format(cls.getModuleName(currItem.parent()),name).lstrip('/')
        else:
            return ''

