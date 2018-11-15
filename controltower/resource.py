import os
from pathlib import Path
import json

class Resource(object):
    def __init__(self):
        self.resourceName = '.athena'
        self.configFileName = '.config'
        self.checkResource()
        self.checkConfig()
        self.checkBoxDirConfigured()

    def checkResource(self):
        """ Check if there's a resource directory.
            If there's no such directory, create one in user home directory
        """
        resource_path_name = '{}/{}'.format(Path.home(),self.resourceName)
        if not os.path.exists(resource_path_name):
            os.makedirs(resource_path_name)

        resource_path_name = '{}/{}/temp'.format(Path.home(),self.resourceName)
        if not os.path.exists(resource_path_name):
            os.makedirs(resource_path_name)

        resource_path_name = '{}/{}/artifacts'.format(Path.home(),self.resourceName)
        if not os.path.exists(resource_path_name):
            os.makedirs(resource_path_name)

    def checkConfig(self):
        cfg_path_name = '{}/{}/{}'.format(Path.home(),self.resourceName,self.configFileName)
        if not os.path.exists(cfg_path_name):
            self.createConfigFile(cfg_path_name)

    def createConfigFile(self,pathName):
        data = {'local_box_storage':'', 'workspace':'{}/{}/artifacts'.format(Path.home(),self.resourceName), 'temp':'{}/{}/temp'.format(Path.home(),self.resourceName)}
        with open(pathName, 'w') as outfile:
            json.dump(data, outfile)

    def updateConfigFile(self,path_name):
        cfg_path_name = '{}/{}/{}'.format(Path.home(), self.resourceName, self.configFileName)
        data = {'local_box_storage':'{}'.format(path_name), 'workspace':'{}/{}/artifacts'.format(Path.home(),self.resourceName), 'temp':'{}/{}/temp'.format(Path.home(),self.resourceName)}
        with open(cfg_path_name, 'w') as outfile:
            json.dump(data, outfile)
        
    def checkBoxDirConfigured(self):
        cfg_path_name = '{}/{}/{}'.format(Path.home(),self.resourceName,self.configFileName)
        with open(cfg_path_name,'r') as f:
            data = json.load(f)
            if not data['local_box_storage']:
                print('LOCAL BOX is not set')
                return False
            else:
                return True

    def getTempDir(self):
        cfg_path_name = '{}/{}/{}'.format(Path.home(), self.resourceName, self.configFileName)
        with open(cfg_path_name, 'r') as f:
            data = json.load(f)
            if data['temp']:
                return data['temp']
            else:
                return ''

    def getWorkspaceDir(self):
        artifact_dir = '{}/{}/artifacts'.format(Path.home(),self.resourceName)
        if os.path.exists(artifact_dir):
            return artifact_dir

    def getLocalWorkSpaceDir(self):
        cfg_path_name = '{}/{}/{}'.format(Path.home(), self.resourceName, self.configFileName)
        with open(cfg_path_name,'r') as f:
            data = json.load(f)
            return data['local_box_storage']
        return ''
