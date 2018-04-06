from PySide2.QtWidgets import QMainWindow, QMenu, QAction

class MainWnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):         
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self) 
        impMenu.addAction(impAct)
        
        newAct = QAction('New', self)        
        
        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        
        self.setWindowTitle('Submenu')    
        self.statusBar().show()
