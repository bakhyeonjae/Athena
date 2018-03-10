from PySide2.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox
from PySide2.QtCore import Qt, QDateTime
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem

class ConfigDialog(QDialog):
    def __init__(self, params = None, parent = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # nice widget for editing the date
        if params:
            row_cnt = len(list(params))
        else:
            row_cnt = 0

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(row_cnt)
        self.tableWidget.setColumnCount(2)

        if params:
            for idx, key in enumerate(list(params)):
                key_name = QTableWidgetItem(key)
                item = QTableWidgetItem(params[key])
                self.tableWidget.setItem(idx,0,key_name)
                self.tableWidget.setItem(idx,1,item)
        
        layout.addWidget(self.tableWidget)
        
        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    # get current date and time from the dialog
    def getParams(self):
        params = {}
        for row in range(self.tableWidget.rowCount()):
            key = self.tableWidget.item(row,0).text()
            val = self.tableWidget.item(row,1).text()
            params[key] = val
        return params

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getParameters(params, parent = None):
        dialog = ConfigDialog(params, parent)
        result = dialog.exec_()
        params = dialog.getParams()
        return (params, result == QDialog.Accepted)
