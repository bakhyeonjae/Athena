from PySide2.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox, QLineEdit, QLabel, QTextEdit, QHBoxLayout
from PySide2.QtCore import Qt, QDateTime

import sys

sys.path.append('..')
sys.path.append('../..')

from src.frontend.infoview import InfoView

class DocumentDialog(QDialog):
    """
    There're 4 sections.
    Description
    Input ports
    Output ports
    Config variables
    """
    def __init__(self, desc, portin, portout, configvar, parent = None):
        super().__init__(parent)

        self.preview = InfoView()
    
        mlayout = QVBoxLayout(self)
        hlayout = QHBoxLayout(self)

        layout = QVBoxLayout()
        
        layout.addWidget(QLabel('Description'))
        self.textDesc = QTextEdit()
        self.textDesc.setText(desc)
        layout.addWidget(self.textDesc)
        self.textDesc.textChanged.connect(lambda:self.genPreview())

        layout.addWidget(QLabel('Input Ports'))
        self.textInput = QTextEdit()
        self.textInput.setText(portin)
        layout.addWidget(self.textInput)
        self.textInput.textChanged.connect(lambda:self.genPreview())

        layout.addWidget(QLabel('Output Ports'))
        self.textOutput = QTextEdit()
        self.textOutput.setText(portout)
        layout.addWidget(self.textOutput)
        self.textOutput.textChanged.connect(lambda:self.genPreview())

        layout.addWidget(QLabel('Config Variables'))
        self.textCfgVar = QTextEdit()
        self.textCfgVar.setText(configvar)
        layout.addWidget(self.textCfgVar)
        self.textCfgVar.textChanged.connect(lambda:self.genPreview())

        hlayout.addLayout(layout)

        infoLayout = QVBoxLayout(self)
        infoLayout.addWidget(QLabel('Preview'))
        infoLayout.addWidget(self.preview)
        hlayout.addLayout(infoLayout)
        mlayout.addLayout(hlayout)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        mlayout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def getResult(self):
        return self.textDesc.toPlainText(), self.textInput.toPlainText(), self.textOutput.toPlainText(), self.textCfgVar.toPlainText()

    @staticmethod
    def getText(desc, portin, portout, cfg, parent = None):
        dialog = DocumentDialog(desc, portin, portout, cfg, parent)
        result = dialog.exec_()
        desc, inport, outport, cfg = dialog.getResult()
        return (desc, inport, outport, cfg, result == QDialog.Accepted)

    def genPreview(self):
        whole_markdown = self.textDesc.toPlainText() + self.textInput.toPlainText() + self.textOutput.toPlainText() + self.textCfgVar.toPlainText()
        self.preview.displayBoxDescription(whole_markdown)
