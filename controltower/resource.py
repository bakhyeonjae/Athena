import os
from pathlib import Path
import json

class Resource(object):
    def __init__(self):
        self.resourceName = '.athena'
        self.configFileName = '.config'
        self.checkResource()
        self.checkConfig()
        self.loadConfig()

    def checkResource(self):
        """ Check if there's a resource directory.
            If there's no such directory, create one in user home directory
        """
        resource_path_name = '{}/{}'.format(Path.home(),self.resourceName)
        if not os.path.exists(resource_path_name):
            os.makedirs(resource_path_name)

    def checkConfig(self):
        cfg_path_name = '{}/{}/{}'.format(Path.home(),self.resourceName,self.configFileName)
        if not os.path.exists(cfg_path_name):
            self.createConfigFile(cfg_path_name)

    def createConfigFile(self,pathName):
        data = {'local_box_storage':'', 'workspace':'{}/artifacts'.format(Path.home())}
        with open(pathName, 'w') as outfile:
            json.dump(data, outfile)
        
    def loadConfig(self):
        cfg_path_name = '{}/{}/{}'.format(Path.home(),self.resourceName,self.configFileName)
        with open(cfg_path_name,'r') as f:
            data = json.load(f)
            if not data['local_box_storage']:
                print('LOCAL BOX is not set')
