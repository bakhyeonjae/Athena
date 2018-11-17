import sys
import os
import requests
import json

sys.path.append('../..')

from framework.util.compressor import Compressor

class SyncBox(object):
    def __init__(self, resource):
        self.resource = resource

    def moveBoxToRepo(self, boxPath):
        compressor = Compressor()
        compressed = compressor.compress('{}/{}'.format(self.resource.getLocalWorkSpaceDir(),boxPath),self.resource.getTempDir())
        url = 'http://localhost:5000/workspace/post'
        data = {'path':'basic/math', 'name':'Const', 'ver':'0.0.1'}
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
        self.requestFile(file_list[0])
        
    def requestFile(self,filename):
        url = 'http://localhost:5000/workspace/box/{}'.format(filename)
        res = requests.get(url)
        with open('tmp.zip', 'wb') as f:
            f.write(res.content)
