class DocumentComposer(object):
    def __init__(self, fileName):
        self.sections = {'[Title]', '[Description]', '[Port : In]', '[Port : Out]', '[Config Variables]'}
        self.fileName = fileName
        self.descText = {}
        for section in self.sections:
            self.descText[section] = ''
        self.loadSections()

    def loadSections(self):
        with open(self.fileName, 'r') as f:
            lines = f.readlines()
        current_section = ''
        for line in lines:
            if line.replace('\n','') in self.sections:
                current_section = line.replace('\n','')
            else:
                self.descText[current_section] += line

    def compose(self, desc, portout, portin, config):
        self.setDesc(desc)
        self.setInText(portin)
        self.setOutText(portout)
        self.setConfigText(config)
        with open(self.fileName, 'w') as f:
            for section in self.sections:
                f.write(section)
                f.write('\n')
                f.write(self.descText[section])
                f.write('\n')
    
    def getDesc(self):
        return self.descText['[Description]']
    def setDesc(self, text):
        self.descText['[Description]'] = text

    def getInText(self):
        return self.descText['[Port : In]']
    def setInText(self, text):
        self.descText['[Port : In]'] = text

    def getOutText(self):
        return self.descText['[Port : Out]']
    def setOutText(self, text):
        self.descText['[Port : Out]'] = text

    def getConfigText(self):
        return self.descText['[Config Variables]']
    def setConfigText(self, text):
        self.descText['[Config Variables]'] = text

    def getBoxName(self):
        return self.descText['[Title]']
    def setBoxName(self, name):
        self.descText['[Title]'] = name
