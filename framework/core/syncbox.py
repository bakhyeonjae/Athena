import sys
import os
import requests

sys.path.append('../..')

from framework.util.compressor import Compressor

class SyncBox(object):
    def __init__(self, resource):
        self.resource = resource

    def moveBoxToRepo(self, boxPath):
        compressor = Compressor()
        compressed = compressor.compress('{}/{}'.format(self.resource.getLocalWorkSpaceDir(),boxPath),self.resource.getTempDir())
        url = 'http://localhost:5000/workspace/put'
        files = {'upload_file':open('{}'.format(compressed),'rb')}
        response = requests.post(url, files=files)
        os.remove(compressed)

    def syncWorkspace(self):
        pass
