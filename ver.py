# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crud.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(986, 508)
        self.btn_nuevo = QtWidgets.QPushButton(Form)
        self.btn_nuevo.setGeometry(QtCore.QRect(20, 30, 86, 27))
        self.btn_nuevo.setObjectName("btn_nuevo")
        self.lista = QtWidgets.QTableWidget(Form)
        self.lista.setGeometry(QtCore.QRect(370, 20, 571, 461))
        self.lista.setStyleSheet("")
        self.lista.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.lista.setTextElideMode(QtCore.Qt.ElideRight)
        self.lista.setObjectName("lista")
        self.lista.setColumnCount(4)
        self.lista.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.lista.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.lista.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.lista.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.lista.setHorizontalHeaderItem(3, item)
        self.lista.horizontalHeader().setCascadingSectionResizes(False)
        self.lista.horizontalHeader().setStretchLastSection(True)
        self.lista.verticalHeader().setVisible(False)
        self.lbl_nombre = QtWidgets.QLabel(Form)
        self.lbl_nombre.setGeometry(QtCore.QRect(30, 90, 64, 19))
        self.lbl_nombre.setObjectName("lbl_nombre")
        self.input_nombre = QtWidgets.QLineEdit(Form)
        self.input_nombre.setEnabled(False)
        self.input_nombre.setGeometry(QtCore.QRect(110, 90, 201, 27))
        self.input_nombre.setObjectName("input_nombre")
        self.lbl_apellidos = QtWidgets.QLabel(Form)
        self.lbl_apellidos.setGeometry(QtCore.QRect(30, 130, 64, 19))
        self.lbl_apellidos.setObjectName("lbl_apellidos")
        self.lbl_dni = QtWidgets.QLabel(Form)
        self.lbl_dni.setGeometry(QtCore.QRect(30, 170, 64, 19))
        self.lbl_dni.setObjectName("lbl_dni")
        self.input_apellidos = QtWidgets.QLineEdit(Form)
        self.input_apellidos.setEnabled(False)
        self.input_apellidos.setGeometry(QtCore.QRect(110, 130, 201, 27))
        self.input_apellidos.setObjectName("input_apellidos")
        self.input_dni = QtWidgets.QLineEdit(Form)
        self.input_dni.setEnabled(False)
        self.input_dni.setGeometry(QtCore.QRect(110, 170, 201, 27))
        self.input_dni.setObjectName("input_dni")
        self.btn_guardar = QtWidgets.QPushButton(Form)
        self.btn_guardar.setEnabled(False)
        self.btn_guardar.setGeometry(QtCore.QRect(20, 220, 86, 27))
        self.btn_guardar.setObjectName("btn_guardar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_nuevo.setText(_translate("Form", "Nuevo"))
        item = self.lista.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ID"))
        item = self.lista.horizontalHeaderItem(1)
        item.setText(_translate("Form", "NOMBRE"))
        item = self.lista.horizontalHeaderItem(2)
        item.setText(_translate("Form", "APELLIDOS"))
        item = self.lista.horizontalHeaderItem(3)
        item.setText(_translate("Form", "DNI"))
        self.lbl_nombre.setText(_translate("Form", "Nombre:"))
        self.lbl_apellidos.setText(_translate("Form", "Apellidos:"))
        self.lbl_dni.setText(_translate("Form", "DNI:"))
        self.btn_guardar.setText(_translate("Form", "Guardar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
