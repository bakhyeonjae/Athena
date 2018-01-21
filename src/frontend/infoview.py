from PySide2.QtWidgets import *
#from PySide2.QtWebKitWidgets import QWebView

class InfoView(QLabel):
    def __init__(self):
        super().__init__()

    def setControlTower(self, ct):
        self.controlTower = ct

    def displayBoxDescription(self, content):
        self.setText(content)

