import os,sys,inspect
import importlib
import math

from boxloader import BoxLoader
from portcore import *
from edgecore import Edge

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

    def createEdge(self, port):
        """
        Args:
            port : PortCore
        """
        if self.isOpened:
            #port.edgeIn = Edge()
            edge = Edge()
            if isinstance(port,PortIn):
                edge.source = port
            elif isinstance(port,PortOut):
                edge.target = port
            port.edgeIn = edge
        else:
            #port.edgeOut = Edge()
            edge = Edge()
            if isinstance(port,PortIn):
                edge.target = port
            elif isinstance(port,PortOut):
                edge.source = port
            port.edgeOut = edge
    
        #if not port.edge:
        #    port.edge = Edge()

    def setName(self,name):
        self.name = name
        if self.view:
            self.view.setName(self.name)

    def openBox(self):
        """
        Set widget's flag to show and resize to dock it in workspace and show child boxes.
        """
        self.isOpened = True
        self.controlTower.openBox(self)
        self.climbToShow()
        # Suppose that ancestor(parent) widget is docked in workspace and its size is full size.
        if self.ancestor:
            width = self.ancestor.view.size().width()
            height = self.ancestor.view.size().height()
            self.view.move(0,0)
            self.view.resize(width,height)
        # Show all the child boxes.
        for box in self.boxes:
            box.view.setAsBlackBox()
            box.view.show()
        self.view.hideTitles()

    def climbToShow(self):
        if self.ancestor:
            self.ancestor.climbToShow()
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
        
        for out_port in outputs:
            new_port = PortOut(self,out_port['name'])
            self.outputs.append(new_port)

        self.view = CommonModuleBox(self,self.viewContainter,self.inputs,self.outputs,'',self.spec)

        for idx, subbox in enumerate(subboxes):
            file_path = BoxLoader.findModuleNameByBoxID(subbox['type'])
            class_name = '{}.box'.format(file_path.split('/')[-1]) 
            module_name = '/'.join(file_path.split('/')[:-1])
            new_box = BoxLoader.createBox(module_name,class_name,self,self.controlTower)
            new_box.setName(subbox['name'])
            
            if self.isOpened:
                new_box.view.show()
            else:
                new_box.view.hide()

            # TODO : Analyse sub-box spec and find box spec.
            # And then create box with the box specs.
            self.boxes.append(new_box)

            outputs = subbox['out-port']
            for out_port in outputs:
                source_port = self.findPortByName('{}@{}'.format(out_port['name'],subbox['name']))
                target_port = self.findPortByName(out_port['connect'])
                print('desc, {} - {}'.format('{}@{}'.format(out_port['name'],subbox['name']),out_port['connect']))
                print('ports : {}.{}'.format(source_port,target_port))
                if target_port and source_port:
                    edge = Edge()
                    edge.connectPorts(source_port, target_port, edgeTgtDir='IN')


        # connect all the ports and logic or boxes
        for in_port in inputs:
            new_port = PortIn(self,in_port['name'])
            new_port.configFromDesc(in_port)
            target_port = self.findPortByName(in_port['connect'])
            if target_port and new_port:
                edge = Edge()
                edge.connectPorts(new_port, target_port, edgeSrcDir='IN') 
            self.inputs.append(new_port)

        self.view.setInputPorts(self.inputs)
        self.view.update()
        
    def findPortByName(self,name):
        tokens = name.split('@')
        port_name = tokens[0]
        if len(tokens) > 1:
            subbox_name = tokens[1]
            
            for box in self.boxes:
                if box.name == subbox_name:
                    for port in box.inputs:
                        if port.name == port_name:
                            return port
                    for port in box.outputs:
                        if port.name == port_name:
                            return port

        for port in self.inputs:
            if port.name == port_name:
                return port

        for port in self.outputs:
            if port.name == port_name:
                return port        

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
        
