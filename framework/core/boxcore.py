
class Box(object):
    def __init__(self, desc):
        self.desc = desc
		self.boxes = []
        self.inputs = []
        self.outputs = []
        self.name = ''
        self.type = ''
		self.view = None

    def constructFromDesc(self,desc):
        box = desc['box']
        subboxes = box['sub-box']
        inputs   = box['in-port']
        outputs  = box['out-port']

        for subbox in box['sub-box']:
            boxes.append(CommonModuleBox(container,len(subbox['in-port']),len(subbox['out-port']),subbox['name'],subbox['type']))

        return boxes

