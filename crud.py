# sqlite > CREATE TABLE personas(
#   ... > id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#   ... > nombre TEXT NOT NULL,
#   ... > apellidos TEXT NOT NULL,
#   ... > dni TEXT NOT NULL);


from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
import sqlite3

app = QtWidgets.QApplication([])
dlg = uic.loadUi('crud.ui')

num_row = 0
# Zona funciones


def prueba():
    print('yesss')


def desbloquear_input():
    dlg.input_nombre.setDisabled(False)
    dlg.input_apellidos.setDisabled(False)
    dlg.input_dni.setDisabled(False)


def bloquear_input():
    dlg.input_nombre.setDisabled(True)
    dlg.input_apellidos.setDisabled(True)
    dlg.input_dni.setDisabled(True)


def conectar():  # Conectar db
    con = sqlite3.connect('personas.db')
    cursor = con.cursor()
    result = cursor.execute('select * from personas')
    for num_row, items in enumerate(result):
        print(items)
        dlg.lista.insertRow(num_row)
        for num_col, dato in enumerate(items):
            cell = QtWidgets.QTableWidgetItem(str(dato))
            cell.setTextAlignment(QtCore.Qt.AlignCenter)
            dlg.lista.setItem(num_row, num_col, cell)


def validoDNI(dni):
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros]) \
            and tabla[int(dni) % 23] == dig_control
    return False


def comprobarGuardar():
    if len(dlg.input_nombre.text()) > 2 and len(dlg.input_apellidos.text()) > 2 and validoDNI(dlg.input_dni.text()):
        dlg.btn_guardar.setDisabled(False)
    else:
        dlg.btn_guardar.setDisabled(True)


def nuevo():
    desbloquear_input()
    dlg.btn_cancelar.setDisabled(False)


def borrarTabla():
    while dlg.lista.rowCount() > 0:
        dlg.lista.removeRow(0)


def refresh():
    borrarTabla()
    conectar()


def guardar():
    con = sqlite3.connect('personas.db')
    cursor = con.cursor()
    nombre = dlg.input_nombre.text()
    apellidos = dlg.input_apellidos.text()
    dni = dlg.input_dni.text()
    query = "INSERT INTO personas (nombre,apellidos,dni) VALUES ('" + \
        nombre+"','"+apellidos+"','"+dni+"')"
    cursor.execute(query)
    con.commit()
    cursor.close()
    refresh()
    dlg.input_nombre.setText('')
    dlg.input_apellidos.setText('')
    dlg.input_dni.setText('')
    bloquear_input()


def cancelar():
    dlg.input_nombre.setText('')
    dlg.input_apellidos.setText('')
    dlg.input_dni.setText('')
    bloquear_input()
    dlg.btn_cancelar.setDisabled(True)


def rowSelected():
    fila = str(dlg.lista.selectedItems()[0].text())
    con = sqlite3.connect('personas.db')
    cursor = con.cursor()
    query = "DELETE FROM personas where ID=" + fila + ""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("This is a message box")
    msg.setInformativeText("This is additional information")
    msg.setWindowTitle("MessageBox demo")
    msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.addButton(QMessageBox.No)

    respuesta = msg.exec_()
    if respuesta == QMessageBox.Ok:
        print('Borra')
    else:
        print('Cancela')
    # cursor.execute(query)
    # con.commit()
    # cursor.close()
    refresh()


def salir():
    app.closeAllWindows()

    # Zona asociación funciones
dlg.btn_nuevo.clicked.connect(nuevo)
dlg.input_nombre.textChanged.connect(comprobarGuardar)
dlg.input_apellidos.textChanged.connect(comprobarGuardar)
dlg.input_dni.textChanged.connect(comprobarGuardar)
dlg.btn_guardar.clicked.connect(guardar)
dlg.btn_cancelar.clicked.connect(cancelar)
dlg.lista.clicked.connect(rowSelected)


dlg.btn_salir.clicked.connect(salir)
conectar()


dlg.show()
app.exec()
