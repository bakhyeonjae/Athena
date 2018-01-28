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
    def __init__(self, desc, ancestor, boxspec, controlTower, view=None):
        self.desc = desc
        self.boxes = []   # type : boxcore.Box
        self.inputs = []
        self.outputs = []
        self.name = ''
        self.type = ''
        if view:
            self.viewContainter = view
        else:
            self.viewContainter = ancestor.view
        self.controlTower = controlTower
        self.logic = None
        self.spec = boxspec
        self.isOpened = False
        self.ancestor = ancestor

        self.buildStructure()

    def openBox(self):
        """
        Set widget's flag to show and resize to dock it in workspace and show child boxes.
        """
        self.isOpened = True
        self.controlTower.openBox(self)
        self.climbToShow()
        # Suppose that ancestor(parent) widget is docked in workspace and its size is full size.
        width = self.ancestor.view.size().width()
        height = self.ancestor.view.size().height()
        self.view.move(0,0)
        self.view.resize(width,height)
        # Show all the child boxes.
        for box in self.boxes:
            box.view.show()
        self.view.hideTitles()

    def climbToShow(self):
        if self.ancestor:
            self.ancestor.climbToShow()
        print('{}'.format(self.view))
        self.view.show()
    
    def openParentBox(self):
        if self.ancestor:
            self.closeBox()
            self.ancestor.openBox()

    def closeBox(self):
        self.isOpened = False
        for box in self.boxes:
            box.view.hide()
        self.view.hide()

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

        self.view = CommonModuleBox(self,self.viewContainter,self.inputs,self.outputs,'',self.spec)

        for idx, subbox in enumerate(subboxes):
            file_path = BoxLoader.findModuleNameByBoxID(subbox['type'])
            class_name = '{}.box'.format(file_path.split('/')[-1]) 
            module_name = '/'.join(file_path.split('/')[:-1])
            new_box = BoxLoader.createBox(module_name,class_name,self,self.controlTower)

            if self.isOpened:
                new_box.view.show()
            else:
                new_box.view.hide()

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
        
