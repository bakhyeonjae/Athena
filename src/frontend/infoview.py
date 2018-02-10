from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView


class InfoView(QWebEngineView):
    def __init__(self, html):
        super().__init__()
        self.setHtml(html)

    def setControlTower(self, ct):
        self.controlTower = ct

    def displayBoxDescription(self, content):
        self.setText(content)

