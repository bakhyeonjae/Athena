from PySide2.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox, QLabel
from PySide2.QtCore import Qt, QDateTime

class AlertDialog(QDialog):
    def __init__(self, parent = None, text = ''):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # nice widget for editing the date
        self.text = QLabel(text)
        layout.addWidget(self.text)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def show(parent = None,text = ''):
        dialog = AlertDialog(parent,text)
        result = dialog.exec_()
        return (result == QDialog.Accepted)
