from PySide2.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox, QLineEdit, QLabel
from PySide2.QtCore import Qt, QDateTime

class BoxVerPathDlg(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.editBox = QLineEdit()
        msg = QLabel('Specify box hierarchy')
        layout.addWidget(msg)
        layout.addWidget(self.editBox)

        ver_msg = QLabel('Specify version of the box')
        self.ver_text = QLineEdit()
        layout.addWidget(ver_msg)
        layout.addWidget(self.ver_text)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def getResult(self):
        return self.editBox.text(), self.ver_text.text()

    @staticmethod
    def getInfo(parent = None):
        dialog = BoxVerPathDlg(parent)
        result = dialog.exec_()
        path_name, ver_text = dialog.getResult()
        return (path_name, ver_text, result == QDialog.Accepted)

