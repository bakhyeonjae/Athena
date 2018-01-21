import os,sys,inspect
import importlib
import math

#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

from boxloader import BoxLoader
from portcore import *

#parentdir = os.path.dirname(currentdir)
#parentdir = os.path.dirname(parentdir)
#sys.path.insert(0,parentdir) 

sys.path.append('../..')

from src.frontend.Box import CommonModuleBox

class Box(object):
    def __init__(self, containerBox, desc, viewContainer, boxspec, controlTower):
        self.desc = desc
        self.boxes = []   # type : boxcore.Box
        self.inputs = []
        self.outputs = []
        self.name = ''
        self.type = ''
        self.view = None
        self.viewContainter = viewContainer
        self.logic = None
        self.spec = boxspec
        self.isOpened = False
        self.containerBox = containerBox
        self.controlTower = controlTower

        self.buildStructure()

    def openBox(self):
        self.isOpened = True
        self.controlTower.openBox(self)
        self.view.openBox()

    def closeBox(self):
        self.isOpened = False
        for box in self.boxes:
            box.view.parent = None
        self.view.parent = None

    def buildStructure(self):
        if not self.desc:
            self.view = CommonModuleBox(self,self.viewContainter,self.inputs,self.outputs,'',self.spec)
            return

        box = self.desc['box']

        subboxes = []
        inputs   = []
        outputs  = []

        if 'sub-box' in box.keys():
            subboxes = box['sub-box']
        if 'code' in box.keys():
            codespec = box['code']
            classname = codespec['class']
            my_class = getattr(importlib.import_module(self.spec), classname)
            self.instance = my_class()

        if 'in-port' in box.keys():
            inputs   = box['in-port']
        if 'out-port' in box.keys():
            outputs  = box['out-port']

        for in_port in inputs:
            new_port = PortIn(self,in_port['name'])
            new_port.configFromDesc(in_port)
            self.inputs.append(new_port)

        for out_port in outputs:
            new_port = PortOut(self,out_port['name'])
            self.outputs.append(new_port)

        if self.containerBox.isOpened:
            self.view = CommonModuleBox(self,self.viewContainter,self.inputs,self.outputs,'',self.spec)

        for idx, subbox in enumerate(subboxes):
            file_path = BoxLoader.findModuleNameByBoxID(subbox['type'])
            class_name = '{}.box'.format(file_path.split('/')[-1]) 
            module_name = '/'.join(file_path.split('/')[:-1])
            new_box = BoxLoader.createBox(module_name,class_name,self,self.controlTower)

            # TODO : Analyse sub-box spec and find box spec.
            # And then create box with the box specs.
            #new_subbox = Box(subbox, self.view, '', True)  # for test
            self.boxes.append(new_box)
        
        # connect all the ports and logic or boxes

    def run(self):
        self.propagateExecution()
        self.execute()

    def propagateExecution(self):
        for port in self.inputs:
            port.propagateExecution()

    def execute(self):
        self.executeCode()

    def executeCode(self):
        box = self.desc['box']
        exec_str = 'self.instance.{}('.format(self.instance.execute.__name__)
        for idx,port in enumerate(self.inputs):
            if box['code']['class'] != port.targetClass:
                return #Raise exception
            params = [p['name'] for p in box['code']['param']]
            if port.targetParam not in params:
                return #Raise exception
            exec_str += '{}=self.inputs[{}].getData()'.format(port.targetParam,idx)
            if self.inputs[-1] != port:
                exec_str += ','
        exec_str += ')'
        print(exec_str)
        eval(exec_str)

        rets = box['code']['return']
        for ret in rets:
            if ret['name'] in [output.name for output in self.outputs]:
                varname = 'self.instance.{}'.format(ret['name'])
                var = eval(varname)
                out_port = next(output for output in self.outputs if output.name == ret['name'])
                out_port.transferData(var)

    def addBox(self,box):
        self.boxes.append(box)
        box.view.move(500,500)
        
