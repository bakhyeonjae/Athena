from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView

import markdown

class InfoView(QWebEngineView):
    def __init__(self):
        super().__init__()

    def setControlTower(self, ct):
        self.controlTower = ct

    def displayBoxDescription(self, content):
        html = markdown.markdown(content)
        self.setHtml(html)

