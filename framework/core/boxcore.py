import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox

class Box(object):
    def __init__(self, desc, container):
        self.desc = desc
        self.boxes = []   # type : boxcore.Box
        self.inputs = []
        self.outputs = []
        self.name = ''
        self.type = ''
        self.view = None
        self.viewContainter = container
        self.logic = None

        self.buildStructure()

    def buildStructure(self):
        box = self.desc['box']

        subboxes = []
        inputs   = []
        outputs  = []

        if 'sub-box' in box.keys():
            subboxes = box['sub-box']
        if 'code' in box.keys():
            codename = box['code']
        if 'in-port' in box.keys():
            inputs   = box['in-port']
        if 'out-port' in box.keys():
            outputs  = box['out-port']

        for subbox in subboxes:
            #new_subbox = Box(subbox,None)
            self.boxes.append(subbox['name'])
        for in_port in inputs:
            self.inputs.append(in_port)
        for out_port in outputs:
            self.outputs.append(out_port)

        # connect all the ports and logic or boxes

        self.view = CommonModuleBox(self.viewContainter,len(self.inputs),len(self.outputs),'','')

    def execute(self):
        pass
