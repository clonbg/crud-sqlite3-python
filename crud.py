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


def validarDni(nif):
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    numeros = "1234567890"
    respuesta=False
    if (len(nif) == 9):
        letraControl = nif[8].upper()
        dni = nif[:8]
        if ( len(dni) == len( [n for n in dni if n in numeros] ) ):
            if tabla[int(dni)%23] == letraControl:
                respuesta= True
    return respuesta
    


def comprobarInput():
    if len(dlg.input_nombre.text()) > 2 and len(dlg.input_apellidos.text()) > 2 and validarDni(dlg.input_dni.text()):
        dlg.btn_guardar.setDisabled(False)
    else:
        dlg.btn_guardar.setDisabled(True)


def nuevo():
    desbloquear_input()

def salir():
    app.closeAllWindows()

    # Zona asociación funciones
dlg.btn_nuevo.clicked.connect(nuevo)
dlg.input_nombre.textChanged.connect(comprobarInput)
dlg.input_apellidos.textChanged.connect(comprobarInput)
dlg.input_dni.textChanged.connect(comprobarInput)


dlg.btn_salir.clicked.connect(salir)
conectar()

dlg.show()
app.exec()
