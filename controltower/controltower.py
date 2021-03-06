from framework.core.boxcore import Box
from framework.core.boxloader import BoxLoader
from framework.core.boxloader import BoxLoader

class ControlTower(object):
    def __init__(self):
        self.rootBox = None
        self.openedBox = None
        self.workspace = None
        self.infoWnd = None
        self.boxTree = None

    def getRootBox(self):
        return self.rootBox

    def setWorkSpace(self, workspace):
        self.workspace = workspace
        self.workspace.setControlTower(self)

    def setInfoWindow(self, infoWnd):
        self.infoWnd = infoWnd
        self.infoWnd.setControlTower(self)

    def setBoxTree(self, boxTree):
        self.boxTree = boxTree
        self.boxTree.setControlTower(self)

    def constructInitState(self):
        self.rootBox = Box(None,None,None,self,self.workspace)
        self.openedBox = self.rootBox
        self.workspace.dockBox(self.openedBox.view)

    def getOpenedBox(self):
        return self.openedBox

    def openBox(self, box):
        if self.openedBox is not box:
            self.openedBox.closeBox()
        self.openedBox = box

    def createNewBox(self,implType):
        new_box = Box(None, self.openedBox, None, self, implType=implType)
        self.openedBox.addBox(new_box) 
        self.openedBox.view.setFocus()
        new_box.view.rename()

    def createBoxFromDesc(self,selectedBox):
        box_dir = '../../boxes'
        new_box = BoxLoader.createBox('../../boxes{}'.format(BoxLoader.getModuleName(selectedBox)),BoxLoader.findModuleName(box_dir,BoxLoader.getModuleName(selectedBox)),self.openedBox,self)
        self.openedBox.addBox(new_box) 
        self.openedBox.view.setFocus()

