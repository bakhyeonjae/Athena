import os,sys,inspect
import importlib
import math
import traceback
from copy import deepcopy
from subprocess import call

from boxloader import BoxLoader
from portcore import *
from edgecore import Edge

sys.path.append('../..')

from src.frontend.Box import CommonModuleBox
from framework.util.writer import BoxWriter
from framework.core.codenode import CodeNode
from framework.core.topology import Topology
from framework.core.codeexport import CodeGenerator
from framework.core.structcode import CodeStruct
from framework.core.structcode import ParamStruct
from framework.core.structcode import ReturnStruct
from framework.core.codetemplate import CodeTemplate
from framework.core.systemconfig import SystemConfig

sys.path.append(SystemConfig.getLocalWorkSpaceDir())
sys.path.append(SystemConfig.getRepository())
sys.path.append(SystemConfig.getBoxDir())

class Box(object):
    def __init__(self, desc, ancestor, boxspec, controlTower, view=None, implType=''):
        self.desc = desc
        self.boxes = []   # type : boxcore.Box
        self.inputs = []
        self.outputs = []
        self.cfgVars = []
        self.retVals = []
        self.name = ''
        self.type = ''
        if view:
            self.viewContainter = view
        else:
            self.viewContainter = ancestor.view
        self.controlTower = controlTower
        self.logic = None
        self.spec = boxspec
        print('Box initialisation : {}'.format(self.spec))
        self.version = None
        self.isOpened = False
        self.ancestor = ancestor
        self.specNotVisible = ['boxes.','private.','builtin.']
        self.configParams = {}
        self.implType = implType
        self.path_name = ''

        self.buildStructure()

    def updateComponentConfig(self, newParams):
        prev = self.getConfigList()
        changed = []
        for old_param in prev:
            changed = changed + [item for item in newParams if item['name'] == old_param['name'] and item['value'] != old_param['value']]

        if changed:
            for item in changed:
                self.setComponentConfig(item)
        
    def setComponentConfig(self,param):
        new_param = deepcopy(param)
        name_hierarchy = param['name']
        object_list = name_hierarchy.split('.')
        if len(object_list) <= 2:
            if object_list[0] == self.name:
                for cfg in self.cfgVars:
                    if cfg.getName() == object_list[1]:
                        cfg.setData(new_param['value'])
        else:
            if object_list[0] == self.name:
                box_name, new_param['name'] = param['name'].split('.',1)
                for box in self.boxes:
                    box.setComponentConfig(new_param)

    def getConfigList(self):
        config_vars = []
        for cfg in self.cfgVars:
            var = {'spec':self.spec, 'name':cfg.getName(), 'value':cfg.getData()}
            config_vars.append(var)
        for box in self.boxes:
            config_vars = config_vars + box.getConfigList()
        for cfg in config_vars:
            cfg['name'] = '{}.{}'.format(self.name,cfg['name'])
        return config_vars

    def deleteBox(self,box):
        selected = next(x for x in self.boxes if x == box)
        selected.view.setParent(None)
        self.boxes.remove(selected)
        del selected
        self.view.update()

    def editCode(self):

        self.path_name = '{}/{}'.format(SystemConfig.getLocalWorkSpaceDir(),self.spec)

        os.makedirs(self.path_name, exist_ok=True) 
        if not os.path.exists('{}/{}.py'.format(self.path_name,self.codedesc.targetClass)):
            code_template = CodeTemplate()
            code_template.setPath(self.path_name)
            code_template.compose(self.codedesc.targetClass,self.inputs,self.outputs,self.cfgVars)

        cmd_str = ['mvim','{}/{}.py'.format(self.path_name,self.codedesc.targetClass)]
        call(cmd_str)

    def getConfigParams(self):
        return self.configParams

    def setConfigParams(self,params):
        # Add new params
        for key in params.keys():
            self.configParams[key] = params[key]

        # delete removed params
        removal_key = []
        for key in self.configParams.keys():
            if key not in params.keys():
                removal_key.append(key)

        for key in removal_key:
            del self.configParams[key]
       
        for name in self.configParams.keys():
            new_flag = True
            for port in self.cfgVars:
                if port.name == name:
                    port.setData(self.configParams[name])
                    new_flag = False
                    break
            if new_flag:
                new_port = PortConfig(self,name,self.configParams[name])
                self.cfgVars.append(new_port)

        # Update cfg ports on view
        self.view.setConfigParamPorts(self.cfgVars)

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
        if self.view and name != self.view.getName():
            self.view.setName(self.name)

        if 'NOT SPECIFIED' == self.spec:
            self.codedesc = CodeStruct()
            self.codedesc.targetClass = self.name
            self.spec = self.name
            if self.view:
                self.view.setTypeName(self.name)

    def openBox(self):
        """
        Set widget's flag to show and resize to dock it in workspace and show child boxes.
        """
        self.isOpened = True
        self.controlTower.openBox(self)
        self.climbToShow()
        # Suppose that ancestor(parent) widget is docked in workspace and its size is full size.
        if self.ancestor:
            self.view.saveCoordinate()
            width = self.ancestor.view.size().width()
            height = self.ancestor.view.size().height()
            self.view.move(0,0)
            self.view.resize(width,height)
        # Show all the child boxes.
        for box in self.boxes:
            box.view.setAsBlackBox()
            box.view.show()
            box.view.restoreCoordinate()
        # Show config ports
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

    def loadCode(self,pathName,className):
        module_name = '{}.{}'.format(self.spec,className)
        print('module_name:{}, target_class:{}'.format(module_name,self.codedesc.targetClass))
        my_class = getattr(importlib.import_module(module_name), self.codedesc.targetClass)
        self.instance = my_class()

    def loadCodeDescription(self):
        box = self.desc['box']
        self.codedesc = CodeStruct()
        self.codedesc.targetClass = box['code']['class']
        if 'param' in box['code'].keys():
            for p in box['code']['param']:
                param = ParamStruct()
                if 'type' in p.keys():
                    param.type = p['type']
                if 'name' in p.keys():
                    param.name = p['name']
                if 'optional' in p.keys():
                    param.optional = p['optional']
                self.codedesc.params.append(param)
        if 'return' in box['code'].keys():
            for r in box['code']['return']:
                ret = ReturnStruct()
                if 'type' in r.keys():
                    ret.type = r['type']
                if 'name' in r.keys():
                    ret.name = r['name']
                if 'connect' in r.keys():
                    ret.connect = r['connect']
                self.codedesc.returns.append(ret)

    def buildStructure(self):
        if not self.desc:
            self.spec = self.spec if self.spec else 'NOT SPECIFIED'
            self.view = CommonModuleBox(self,self.viewContainter,self.inputs,self.outputs,'',self.spec)
            self.view.configPopupMenu(self.implType)
            return

        box = self.desc['box']

        subboxes = []
        inputs   = []
        outputs  = []

        if 'version' in box.keys():
            self.version = box['version']

        if 'sub-box' in box.keys():
            self.implType = 'COMPOSITION'
            subboxes = box['sub-box']

        if 'code' in box.keys():
            self.loadCodeDescription()
            self.implType = 'CODE'
            print('=========> {}'.format(self.spec))
            my_class = getattr(importlib.import_module(self.spec.replace('.Users.hj.bak.AthenaBoxes.','')), self.codedesc.targetClass)
            self.instance = my_class()
            for ret_val in self.codedesc.returns:
                self.retVals.append({'retName':ret_val.name, 'portname':ret_val.connect})

        if 'in-port' in box.keys():
            inputs   = box['in-port']
        if 'out-port' in box.keys():
            outputs  = box['out-port']
        
        for out_port in outputs:
            new_port = PortOut(self,out_port['name'])
            self.outputs.append(new_port)

        simplified_spec = self.spec
        for remove_spec in self.specNotVisible:
            simplified_spec = simplified_spec.replace(remove_spec,'')
        self.view = CommonModuleBox(self,self.viewContainter,self.inputs,self.outputs,'',simplified_spec)
        self.view.configPopupMenu(self.implType)

        for idx, subbox in enumerate(subboxes):
            file_path = BoxLoader.findModuleNameByBoxID(subbox['type'])
            class_name = '{}.box'.format(file_path.split('/')[-1]) 
            module_name = '/'.join(file_path.split('/')[:-1])
            print('file_path:{}'.format(file_path))
            print('In boxcore.buildStructure - subbox_name:{}, module_name:{}, class_name:{}'.format(subbox['type'],module_name,class_name))
            #new_box = BoxLoader.createBox(module_name,class_name,self,self.controlTower)
            if SystemConfig.getLocalWorkSpaceDir() in module_name:
                only_module_name = module_name.replace(SystemConfig.getLocalWorkSpaceDir(),'')
            elif SystemConfig.getBoxDir() in module_name:
                only_module_name = module_name.replace(SystemConfig.getBoxDir(),'')
            new_box = BoxLoader.createBox(only_module_name.lstrip('/'),class_name,self,self.controlTower)
            new_box.setName(subbox['name'])
            
            if self.isOpened:
                new_box.view.show()
            else:
                new_box.view.hide()

            if 'geometry' in subbox.keys():
                w = self.controlTower.openedBox.view.width()
                h = self.controlTower.openedBox.view.height()
                new_box.view.move(subbox['geometry']['x']*w,subbox['geometry']['y']*h)

            # TODO : Analyse sub-box spec and find box spec.
            # And then create box with the box specs.
            self.boxes.append(new_box)
        for idx, subbox in enumerate(subboxes):
            outputs = subbox['out-port']
            for out_port in outputs:
                source_port = self.findPortByName('{}@{}'.format(out_port['name'],subbox['name']))
                target_port = self.findPortByName(out_port['connect'])
                if target_port and source_port:
                    edge = Edge()
                    if target_port in self.outputs:
                        edge.connectPorts(source_port, target_port, edgeTgtDir='IN')
                    else:
                        edge.connectPorts(source_port, target_port)
                    

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

        # Connect all the config params
        if 'config' in box.keys():
            configParams = box['config']
            for config in configParams:
                self.configParams[config['name']] = config['value']
                new_port = PortConfig(self,config['name'],config['value'])
                new_port.configFromDesc(config)
                target_port = self.findPortByName(config['connect'])
                if target_port and new_port:
                    edge = Edge()
                    edge.connectPorts(new_port,target_port, edgeSrcDir='IN')
                self.cfgVars.append(new_port)
            
        self.view.setConfigParamPorts(self.cfgVars)

        self.view.update()

    def removePort(self,port):
        if port in self.outputs:
            self.view.removePort(port.getView())
            self.outputs.remove(port)
        if port in self.inputs:
            self.view.removePort(port.getView())
            self.inputs.remove(port)
        self.view.update()

    def addOutPort(self,name):
        # Allow a user specify name
        new_port = PortOut(self,name)
        if 'CODE' == self.implType:
            ret = ReturnStruct()
            ret.name = name
            ret.connect = name
            self.codedesc.returns.append(ret)
            new_port.setDescription(ret)
        self.outputs.append(new_port)
        self.view.setOutputPorts(self.outputs)
        self.view.update()

    def addInPort(self,name):
        # Allow a user specify name
        new_port = PortIn(self,name)
        if 'CODE' == self.implType and not new_port.isCodeConfigured():
            new_port.configFromDesc({'connect':'{}@{}'.format(name,self.codedesc.targetClass)})
            param = ParamStruct()
            param.name = name
            self.codedesc.params.append(param)
            new_port.setDescription(param)
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
        print('run - box name is ',self.name)
        self.execute()

    def propagateExecution(self):
        for port in self.inputs:
            port.propagateExecution()

    def execute(self):
        if self.boxes:
            pass
        else:
            print('execute - box name is ',self.name)
            self.executeCode()

    def executeCode(self):
        if '' != self.path_name:
            self.loadCode(self.path_name,self.codedesc.targetClass)
        
        exec_str = 'self.instance.{}('.format(self.instance.execute.__name__)
        for idx,port in enumerate(self.inputs):
            if 'newbox' == self.name:
                print('targetClass : {}, port.targetClass : {}'.format(self.codedesc.targetClass,port.targetClass))
            if self.codedesc.targetClass != port.targetClass:
                return #Raise exception
            params = [p.name for p in self.codedesc.params]
            if 'newbox' == self.name:
                print('targetParam : {}, params : {}'.format(port.targetParam,params))
            if port.targetParam not in params:
                return #Raise exception
            exec_str += '{}=self.inputs[{}].getData()'.format(port.targetParam,idx)
            if self.inputs[-1] != port:
                exec_str += ','
        if self.inputs and self.cfgVars:
            exec_str += ','
        for idx,port in enumerate(self.cfgVars):
            if 'newbox' == self.name:
                print('#targetClass : {}, port.targetClass : {}'.format(self.codedesc.targetClass,port.targetClass))
            if self.codedesc.targetClass != port.targetClass:
                return #Raise exception
            params = [p.name for p in self.codedesc.params]
            if 'newbox' == self.name:
                print('#targetParam : {}, params : {}'.format(port.targetParam,params))
            if port.targetParam not in params:
                return #Raise exception
            exec_str += '{}=self.cfgVars[{}].getData()'.format(port.targetParam,idx)
            if self.cfgVars[-1] != port:
                exec_str += ','
        exec_str += ')'
        eval(exec_str)

        for ret in self.codedesc.returns:
            if ret.name in [output.name for output in self.outputs]:
                varname = 'self.instance.{}'.format(ret.name)
                print('varname = ','self.instance.{}'.format(ret.name))
                var = eval(varname)
                out_port = next(output for output in self.outputs if output.name == ret.name)
                out_port.transferData(var)

    def addBox(self,box):
        self.boxes.append(box)
        box.view.move(500,500)

    def save(self):

        self.path_name = '{}/{}'.format(SystemConfig.getLocalWorkSpaceDir(),self.spec)

        os.makedirs(self.path_name, exist_ok=True) 

        file_name = '{}/{}.box'.format(self.path_name,self.spec)
        writer = BoxWriter(file_name)
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
                if 'CODE' == self.implType:
                    writer.write('\"connect\":\"{}@{}\"'.format(port.name,self.codedesc.targetClass)) 
                else:
                    writer.write('\"connect\":\"{}@{}\"'.format(port.edgeIn.target.name,port.edgeIn.target.box.name)) # only if sub boxes exist
                writer.decIndent()
                if port == self.inputs[-1]:
                    writer.write('}')
                else:
                    writer.write('},')
            writer.decIndent()
            writer.write('],')
        # write code
        if 'CODE' == self.implType:
            writer.write('\"code\":{')
            writer.incIndent()
            writer.write('\"class\":\"{}\",'.format(self.codedesc.targetClass))
            writer.write('\"param\":[')
            writer.incIndent()
            for param in self.codedesc.params:
                writer.write('{')
                writer.write('\"type\":\"{}\",'.format(param.type))
                writer.write('\"name\":\"{}\",'.format(param.name))
                writer.write('\"optional\":\"{}\"'.format(param.optional))
                if param == self.codedesc.params[-1]:
                    if self.cfgVars:
                        writer.write('},')
                    else:
                        writer.write('}')
                else:
                    writer.write('},')
            for config in self.cfgVars:
                writer.write('{')
                writer.incIndent()
                writer.write('\"name\":\"{}\",'.format(config.getName()))
                writer.write('\"value\":\"{}\",'.format(config.getData()))
                writer.write('\"connect\":\"{}@{}\"'.format(config.getName(),self.codedesc.targetClass))
                writer.decIndent()
                if config == self.cfgVars[-1]:
                    writer.write('}')
                else:
                    writer.write('},')
            writer.decIndent()
            writer.write('],')
            writer.write('\"return\":[')
            writer.incIndent()
            for ret in self.codedesc.returns:
                writer.write('{')
                writer.write('\"type\":\"{}\",'.format(ret.type))
                writer.write('\"name\":\"{}\",'.format(ret.name))
                writer.write('\"connect\":\"{}\"'.format(ret.connect))
                if ret == self.codedesc.returns[-1]:
                    writer.write('}')
                else:
                    writer.write('},')
            writer.decIndent()
            writer.write(']')
            writer.decIndent()
            writer.write('},')
            
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
                writer.write('\"geometry\":{')
                writer.incIndent()
                writer.write('\"x\":{},'.format(box.view.getX()/self.view.width()))
                writer.write('\"y\":{}'.format(box.view.getY()/self.view.height()))
                writer.decIndent()
                writer.write('},')
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
                    writer.write('\"connect\":\"{}@{}\"'.format(port.edgeOut.target.name,port.edgeOut.target.box.name))
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

        if len(self.configParams) > 0:
            writer.write('\"config\":[')
            writer.incIndent()
            for config in self.cfgVars:
                writer.write('{')
                writer.incIndent()
                writer.write('\"name\":\"{}\",'.format(config.getName()))
                writer.write('\"value\":\"{}\",'.format(config.getData()))
                if 'CODE' == self.implType:
                    writer.write('\"connect\":\"{}@{}\"'.format(config.getName(),self.codedesc.targetClass))
                else:
                    writer.write('\"connect\":\"{}@{}\"'.format(config.edgeIn.target.name,config.edgeIn.target.box.name))
                writer.decIndent()
                if config == self.cfgVars[-1]:
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

    def isComposition(self):
        return True if 'COMPOSITION' == self.implType else False
   
    def getCodeSpecNode(self,nameParam,outPort):
        node = CodeNode()
        node.setBoxSpec(self.spec) 
        node.setClassName(self.codedesc.targetClass)
        node.setInstanceID(self)
        node.setParamName(nameParam)
        node.setRetName(self.findRetNameByOutputName(outPort))
        return node

    def composeCode(self):
        func_names = []
        module_names = []
        local_dir = './export'
        CodeGenerator.createDir(local_dir) 
        for target_port in self.outputs:
            nameParam = target_port.name
            graph = target_port.constructGraph(nameParam)
            graph.displayGraph()
            
            topology = Topology()
            topology.setGraph(graph)
            ordered = topology.sort()
            exporter = CodeGenerator(local_dir)
            module_name = '{}_{}.py'.format(target_port.name,target_port.box.name).replace(' ','')
            callable_func = exporter.exportCode(target_port,ordered,module_name)
            exporter.transferLibFiles(ordered,local_dir)
            func_names.append(callable_func)
            module_names.append(module_name)
        
        main_module = CodeGenerator(local_dir)
        main_module.exportExampleModule(func_names,module_names)

    def requestGraphToConfigs(self):
        graph = []
        for port_cfg in self.cfgVars:
            name_param = port_cfg.targetParam
            graph.append(port_cfg.constructGraph(name_param))
        return graph

    def requestGraphToInputs(self):
        graph = []
        for port_in in self.inputs:
            name_param = port_in.targetParam
            graph.append(port_in.constructGraph(name_param))
        return graph

    def findRetNameByOutputName(self,outPort):
        for var in self.retVals:
            if var['portname'] == outPort.name:
                return var['retName']
        return None
