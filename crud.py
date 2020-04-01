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


# Abrimos y creeamos el cursor
con = sqlite3.connect('personas.db')
cursor = con.cursor()

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
    result = cursor.execute('select * from personas')
    for num_row, items in enumerate(result):
        print(items)
        dlg.lista.insertRow(num_row)
        for num_col, dato in enumerate(items):
            cell = QtWidgets.QTableWidgetItem(str(dato))
            cell.setTextAlignment(QtCore.Qt.AlignCenter)
            dlg.lista.setItem(num_row, num_col, cell)


def validarDni(dni):
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


def comprobarInputNombre():
    if len(dlg.input_nombre.text()) > 2:
        dlg.btn_guardar.setDisabled(False)
    else:
        dlg.btn_guardar.setDisabled(True)


def nuevo():
    desbloquear_input()

    # Zona asociación funciones
dlg.btn_nuevo.clicked.connect(nuevo)
dlg.input_nombre.textChanged.connect(comprobarInputNombre)

conectar()

dlg.show()
app.exec()
