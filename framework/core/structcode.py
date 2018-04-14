
class CodeStruct(object):
    def __init__(self):
        self.targetClass = ''
        self.params = []
        self.returns = []

class ParamStruct(object):
    def __init__(self):
        self.type = ''
        self.name = ''
        self.optional = ''

class ReturnStruct(object):
    def __init__(self):
        self.type = ''
        self.name = ''
        self.connect = ''
