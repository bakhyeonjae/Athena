import gzip
import shutil
import os

class Compressor(object):
    def __init__(self):
        pass

    def compress(self, pathName, destDir):
        shutil.make_archive('tmp', 'zip', pathName)
        if os.path.exists('{}/tmp.zip'.format(destDir)):
            os.remove('{}/tmp.zip'.format(destDir))
        shutil.move('./tmp.zip', destDir)
        return '{}/tmp.zip'.format(destDir)
