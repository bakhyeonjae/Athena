import os,sys,inspect
import json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir) 
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox
from boxes.builtin.primitives.genrandom import BoxRandomGenerator

class BoxLoader(object):
    def __init__(self):
        pass

    def loadBoxDesc(self, data):
        desc = json.loads(data)
        box = desc['box']
        subboxes = box['sub-box']
        inputs   = box['in-port']
        outputs  = box['out-port']
        return box
	 
    def createBox(self,parent, desc):
        CommonModuleBox(parent,len(desc['in-port']),len(desc['out-port']),desc['name'],desc['type'])

