import sys
import os
import requests
import json

from PySide2.QtWidgets import QDialog

sys.path.append('../..')

from framework.util.compressor import Compressor
from src.frontend.boxverpathdlg import BoxVerPathDlg

class SyncBox(object):
    def __init__(self, resource):
        self.resource = resource

    def moveBoxToRepo(self, boxPath):
        compressor = Compressor()
        compressed = compressor.compress('{}/{}'.format(self.resource.getLocalWorkSpaceDir(),boxPath),self.resource.getTempDir())
        url = 'http://localhost:5000/workspace/post'
        user_path, user_ver, ret = BoxVerPathDlg.getInfo()
        path, name = os.path.split(boxPath)
        if QDialog.Accepted == ret:
            data = {'path':user_path, 'name':name, 'ver':user_ver.replace('.','_')}
            files = {
                    'spec':('spec', json.dumps(data), 'application/json'),
                    'file':(os.path.basename(compressed), open('{}'.format(compressed),'rb'), 'application/octet-stream')
            }
        response = requests.post(url, files=files)
        os.remove(compressed)
        
    def syncWorkspace(self):
        url = 'http://localhost:5000/workspace/list'
        response = requests.get(url)
        res = json.loads(response.text)
        file_list = res['boxes']
        for f in file_list:
            self.requestFile(f, self.resource.getWorkspaceDir())
        
    def requestFile(self, pathName, baseDir):
        url = 'http://localhost:5000/workspace/box/{}'.format(pathName)
        res = requests.get(url)
        path_name, file_name = os.path.split(pathName)
        if not os.path.exists('{}/{}'.format(baseDir, path_name)):
            os.makedirs('{}/{}'.format(baseDir,path_name))
        with open('{}/{}/{}'.format(baseDir, path_name, file_name), 'wb') as f:
            f.write(res.content)
        compressor = Compressor()
        compressor.decompress('{}/{}/{}'.format(baseDir, path_name, file_name))
