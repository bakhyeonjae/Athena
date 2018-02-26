class BoxWriter(object):
    def __init__(self, fileName):
        self.fo = open(fileName, 'w', encoding='utf-8')
        self.cnt = 0

    def incIndent(self):
        self.cnt += 1

    def decIndent(self):
        self.cnt -= 1

    def write(self, sentence):
        str_list = []
        for idx in range(self.cnt):
            str_list.append('    ')
        str_list.append(sentence)
        str_list.append('\n')
        self.fo.write(''.join(str_list))

    def finalise(self):
        self.fo.close()
