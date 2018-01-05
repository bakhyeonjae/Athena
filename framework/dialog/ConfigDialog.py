from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt, QDateTime

class ConfigDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # nice widget for editing the date
        self.dimension= QComboBox()
        self.dimension.addItem('1')
        self.dimension.addItem('2')
        self.dimension.addItem('3')
        layout.addWidget(self.dimension)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    # get current date and time from the dialog
    def getDimension(self):
        return self.dimension.currentIndex() + 1

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getParameters(parent = None):
        dialog = ConfigDialog(parent)
        result = dialog.exec_()
        dimension = dialog.getDimension()
        return (dimension, result == QDialog.Accepted)
