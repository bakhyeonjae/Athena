from framework.core.codeexport import CodeGenerator
from framework.core.codenode import CodeNode
from framework.core.topology import Topology

class Exporter(object):
    def __init__(self):
        pass

    def search(self, rootBox):
        port_list = []
        for box in rootBox.boxes:
            for iport in box.inputs:
                if iport.getExportFlag():
                    port_list.append(iport)
            for oport in box.outputs:
                if oport.getExportFlag():
                    port_list.append(oport)
        return port_list

    def processExport(self, openedBox):
        ports = self.search(openedBox)
        for port in ports:
            print(port.name)

            func_names = []
            module_names = []
            local_dir = './export'
            CodeGenerator.createDir(local_dir) 
            for target_port in ports:
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

