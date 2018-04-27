from PySide2.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox, QPushButton, QHBoxLayout
from PySide2.QtCore import Qt, QDateTime
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from PySide2.QtWidgets import QAbstractItemView

class GlobalConfigDialog(QDialog):
    def __init__(self, params = None, parent = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        if params:
            row_cnt = len(list(params))
        else:
            row_cnt = 0

        self.new_param_idx = 0
        self.tableWidget = QTableWidget()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(row_cnt)
        self.tableWidget.setColumnCount(3)

        if params:
            self.tableWidget.setHorizontalHeaderLabels(list(params[0].keys()))
            for row, param in enumerate(params):
                for idx, key in enumerate(list(param)):
                    item = QTableWidgetItem(param[key])
                    self.tableWidget.setItem(row,idx,item)
        layout.addWidget(self.tableWidget)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def getParams(self):
        params = []
        keys = []

        num_columns = self.tableWidget.columnCount()
        for idx in range(num_columns):
            keys.append(self.tableWidget.horizontalHeaderItem(idx).text())
        
        for row in range(self.tableWidget.rowCount()):
            param = {}
            for idx in range(num_columns):
                val = self.tableWidget.item(row,idx).text()
                param[keys[idx]] = val
            params.append(param)
        return params

    @staticmethod
    def getParameters(params, parent = None):
        dialog = GlobalConfigDialog(params, parent)
        result = dialog.exec_()
        params = dialog.getParams()
        return (params, result == QDialog.Accepted)
