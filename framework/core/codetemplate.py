
class CodeTemplate(object):
    def __init__(self):
        pass

    def setPath(self,path):
        self.pathName = path

    def compose(self, className, portIn, portOut):
        self.className =  className

        with open('{}/{}.py'.format(self.pathName,self.className),'w') as of:
            of.write('class {}(object):\n'.format(self.className))
            of.write('    def __init__(self):\n')
            of.write('        pass\n')
            of.write('\n')
            func_def = '    def execute(self'
            for iport in portIn:
                func_def += ','
                func_def += iport.name
            func_def += '):\n'
            of.write(func_def)
            indentation = '        '
            for oport in portOut:
                ret_str = '{}self.{}\n'.format(indentation,oport.name)
                of.write(ret_str)
