class DescTemplate(object):
    def __init__(self):
        pass

    def setPath(self, path):
        self.pathName = path

    def compose(self, className, portIn, portOut, cfgs):
        with open('{}/desc.md'.format(self.pathName), 'w') as of:
            of.write('[Title]\n{}\n'.format(className))
            of.write('[Description]\n')
            of.write('[Port : In]\n')
            for iport in portIn:
                of.write('    {} : \n'.format(iport.name))
            of.write('[Port : Out]\n')
            for oport in portOut:
                of.write('    {} : \n'.format(oport.name))
            of.write('[Config Variables]\n')
            for cfg in cfgs:
                of.write('    {} : \n'.format(cfg.name))

