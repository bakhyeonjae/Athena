from PySide2.QtWidgets import QMainWindow, QMenu, QAction
from PySide2.QtWidgets import QPushButton, QMenuBar

import sys

from framework.core.exporter import Exporter

class MainWnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.exporter = Exporter()
        self.initUI()
        
    def initUI(self):         

        self.menuBar= QMenuBar(self)
        self.menuBar.setNativeMenuBar(False)
        
        file_menu = self.menuBar.addMenu('File')
        file_menu.addAction('New',self.save)
        file_menu.addAction('Open',self.save)
        file_menu.addAction('Close',self.save)
        file_menu.addAction('Save',self.save)
        file_menu.addAction('Save as',self.save)
        file_menu.addAction('Quit',self.quit)

        repo_menu = self.menuBar.addMenu('Repository')
        repo_menu.addAction('private')
        repo_menu.addAction('global')

        config_menu = self.menuBar.addMenu('Tools')
        config_menu.addAction('Preferences')
        config_menu.addAction('Export',self.exporter.processExport)

        window_menu = self.menuBar.addMenu('Window')
        window_menu.addAction('Description')

        help_menu = self.menuBar.addMenu('Help')
        help_menu.addAction('online document',self.quit)

        self.setMenuBar(self.menuBar)

        self.setWindowTitle('Athena')
        self.statusBar().show()

    def save(self):
        exporter = Exporter()
        exporter.processExport()

    def quit(self):
        sys.exit(0)

