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


def conectar():  # Conectar db
    result = cursor.execute('select * from personas')
    for num_row, items in enumerate(result):
        print(items)
        dlg.lista.insertRow(num_row)
        for num_col, dato in enumerate(items):
            cell = QtWidgets.QTableWidgetItem(str(dato))
            cell.setTextAlignment(QtCore.Qt.AlignCenter)
            dlg.lista.setItem(num_row, num_col, cell)


def nuevo():  # nueva persona



    # Zona asociación funciones

dlg.btn_nuevo.clicked.connect(prueba)

conectar()

dlg.show()
app.exec()
