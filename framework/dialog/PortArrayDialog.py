from PySide2.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox, QLineEdit, QLabel
from PySide2.QtCore import Qt, QDateTime

class PortArrayDialog(QDialog):
    def __init__(self, message, parent = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.editBox = QLineEdit()
        self.numberPort = QLineEdit()
        msg = QLabel(message)
        layout.addWidget(msg)
        layout.addWidget(self.editBox)
        layout.addWidget(QLabel('number of ports'))
        layout.addWidget(self.numberPort)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    # get current date and time from the dialog
    def getResult(self):
        return self.editBox.text(), self.numberPort.text()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getParameters(message, parent = None):
        dialog = PortArrayDialog(message, parent)
        result = dialog.exec_()
        text, number = dialog.getResult()
        return (text, int(number), result == QDialog.Accepted)
