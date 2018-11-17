import gzip
import shutil
import os

BOX_PACKAGE_NAME = 'box'

class Compressor(object):
    def __init__(self):
        pass

    def compress(self, pathName, destDir):
        shutil.make_archive(BOX_PACKAGE_NAME, 'zip', pathName)
        if os.path.exists('{}/{}.zip'.format(destDir,BOX_PACKAGE_NAME)):
            os.remove('{}/{}.zip'.format(destDir,BOX_PACKAGE_NAME))
        shutil.move('./{}.zip'.format(BOX_PACKAGE_NAME), destDir)
        return '{}/{}.zip'.format(destDir,BOX_PACKAGE_NAME)
