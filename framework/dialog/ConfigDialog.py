from PySide2.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox, QPushButton, QHBoxLayout
from PySide2.QtCore import Qt, QDateTime
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from PySide2.QtWidgets import QAbstractItemView

class ConfigDialog(QDialog):
    def __init__(self, params = None, parent = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # nice widget for editing the date
        if params:
            row_cnt = len(list(params))
        else:
            row_cnt = 0

        self.new_param_idx = 0
        self.tableWidget = QTableWidget()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(row_cnt)
        self.tableWidget.setColumnCount(2)

        if params:
            for idx, key in enumerate(list(params)):
                key_name = QTableWidgetItem(key)
                item = QTableWidgetItem(params[key])
                self.tableWidget.setItem(idx,0,key_name)
                self.tableWidget.setItem(idx,1,item)
       
        button_add = QPushButton('+',self)
        button_add.clicked.connect(self.addParam)
        button_del = QPushButton('-',self)
        button_del.clicked.connect(self.delParam)

        control_layout = QHBoxLayout(self)
        control_layout.addWidget(button_add)
        control_layout.addWidget(button_del)

        layout.addLayout(control_layout) 
        layout.addWidget(self.tableWidget)
        
        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def updateTable(self, newParams):
        if not newParams:
            return 

        row_cnt = self.tableWidget.rowCount()
        addition = 0
        for idx, key in enumerate(list(newParams)):
            new_param_flag = True
            for row in range(row_cnt):
                item = self.tableWidget.item(row,0).text()
                if item == key:
                    new_param_flag = False
                    break
            if new_param_flag:
                key_name = QTableWidgetItem(key)
                item = QTableWidgetItem(newParams[key])
                self.tableWidget.insertRow(row_cnt+addition)
                self.tableWidget.setItem(row_cnt+addition,0,key_name)
                self.tableWidget.setItem(row_cnt+addition,1,item)
                addition += 1

    def addParam(self):
        name = 'param_{}'.format(self.new_param_idx)
        self.updateTable({name:''})
        self.new_param_idx += 1

    def delParam(self):
        indices = self.tableWidget.selectionModel().selectedRows()
        for index in indices:
            self.tableWidget.removeRow(index.row())

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
