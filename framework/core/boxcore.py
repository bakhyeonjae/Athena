import os,sys,inspect
import importlib
import math

from boxloader import BoxLoader
from portcore import *
from edgecore import Edge

sys.path.append('../..')

from src.frontend.Box import CommonModuleBox
from framework.util.writer import BoxWriter

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
        self.version = None
        self.isOpened = False
        self.ancestor = ancestor

        self.buildStructure()

    def hasSubBox(self):
        if self.boxes:
            return True
        else:
            return False

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
        self.view.setFocus()  # To get keyboard event 

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

        if 'version' in box.keys():
            self.version = box['version']
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

    def addOutPort(self):
        # Allow a user specify name
        new_port = PortOut(self,'test') 
        self.outputs.append(new_port)
        self.view.setOutputPorts(self.outputs)
        self.view.update()

    def addInPort(self):
        # Allow a user specify name
        new_port = PortIn(self,'test')
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
        print('{}.run'.format(self.spec))
        self.propagateExecution()
        self.execute()

    def propagateExecution(self):
        print('{}.propagateExecution'.format(self.spec))
        for port in self.inputs:
            port.propagateExecution()

    def execute(self):
        print('{}.execute'.format(self.spec))
        if self.boxes:
            pass
        else:
            print(self.spec)
            self.executeCode()

    def executeCode(self):
        print('{}.executeCode'.format(self.spec))
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
            print('port obj:{}'.format(port))
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

    def save(self, fileName):
        writer = BoxWriter(fileName)
        writer.write('{')
        writer.incIndent()
        writer.write('\"box\":{')
        writer.incIndent()
        writer.write('\"version\":\"{}\",'.format(self.version))
        # write inputs
        if self.inputs:
            writer.write('\"in-port\":[')
            writer.incIndent()
            for port in self.inputs:
                writer.write('{')
                writer.incIndent()
                writer.write('\"name\":\"{}\",'.format(port.name))
                writer.write('\"connect\":\"{}@{}\"'.format(port.edgeIn.target.name,port.edgeIn.target.box.name)) # only if sub boxes exist
                writer.decIndent()
                if port == self.inputs[-1]:
                    writer.write('}')
                else:
                    writer.write('},')
            writer.decIndent()
            writer.write('],')
            
        # write boxes
        if self.boxes:
            writer.write('\"sub-box\":[')
            writer.incIndent()
            for box in self.boxes:
                writer.write('{')
                writer.incIndent()
                spec_str = '{}@{}'.format(box.spec.replace('boxes.',''),box.version)
                writer.write('\"type\":\"{}\",'.format(spec_str))
                writer.write('\"name\":\"{}\",'.format(box.name))
                writer.write('\"in-port\":[')
                writer.incIndent()
                for port in box.inputs:
                    writer.write('{')
                    writer.incIndent()
                    writer.write('\"name\":\"{}\"'.format(port.name))
                    writer.decIndent()
                    if port == box.inputs[-1]:
                        writer.write('}')
                    else:
                        writer.write('},')
                writer.decIndent()
                writer.write('],')
                writer.write('\"out-port\":[')
                writer.incIndent()
                for port in box.outputs:
                    writer.write('{')
                    writer.incIndent()
                    writer.write('\"name\":\"{}\",'.format(port.name))
                    writer.write('\"connect\":\"{}\"'.format(port.edgeOut.target.name))
                    writer.decIndent()
                    if port == box.outputs[-1]:
                        writer.write('}')
                    else:
                        writer.write('},')
                writer.decIndent()
                writer.write(']')
                writer.decIndent()
                if box == self.boxes[-1]:
                    writer.write('}')
                else:
                    writer.write('},')
            writer.decIndent()
            writer.write('],')

        # write outputs
        if self.outputs:
            writer.write('\"out-port\":[')
            writer.incIndent()
            for port in self.outputs:
                writer.write('{')
                writer.incIndent()
                writer.write('\"name\":\"{}\"'.format(port.name))
                writer.decIndent()
                if port == self.outputs[-1]:
                    writer.write('}')
                else:
                    writer.write('},')
            writer.decIndent()
            writer.write(']')

        writer.decIndent()
        writer.write('}')
        writer.decIndent()
        writer.write('}')
  
