from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QDateTime

class TextInputDialog(QDialog):
    def __init__(self, message, parent = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.editBox = QLineEdit()
        msg = QLabel(message)
        layout.addWidget(msg)
        layout.addWidget(self.editBox)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    # get current date and time from the dialog
    def getResult(self):
        return self.editBox.text()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getText(message, parent = None):
        dialog = TextInputDialog(message, parent)
        result = dialog.exec_()
        text = dialog.getResult()
        return (text, result == QDialog.Accepted)
