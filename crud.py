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
    dlg.btn_cancelar.setDisabled(True)


def cancelar():
    dlg.input_nombre.setText('')
    dlg.input_apellidos.setText('')
    dlg.input_dni.setText('')
    bloquear_input()
    dlg.btn_cancelar.setDisabled(True)
    dlg.btn_eliminar.setDisabled(True)
    dlg.btn_nuevo.setDisabled(False)
    dlg.btn_editar.setDisabled(True)

def selectTabla():
    dlg.btn_eliminar.setDisabled(False)
    dlg.btn_nuevo.setDisabled(True)
    dlg.btn_cancelar.setDisabled(False)
    bloquear_input()
    dlg.btn_editar.setDisabled(False)
    
    
def eliminar():
    con = sqlite3.connect('personas.db')
    cursor = con.cursor()
    query = "DELETE FROM personas where ID=" + str(dlg.lista.selectedItems()[0].text()) + ""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Acción peligrosa")
    msg.setInformativeText("¿Esta segur@ de que desea eliminar la fila?")
    msg.setWindowTitle("Aviso")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.addButton(QMessageBox.No)
    respuesta = msg.exec_()
    if respuesta == QMessageBox.Ok:
        print('Borra')
        cursor.execute(query)
        con.commit()
        cursor.close()
        refresh()
    else:
        print('Cancela')
    dlg.btn_cancelar.setDisabled(True)
    dlg.btn_eliminar.setDisabled(True)
    dlg.btn_nuevo.setDisabled(False)
    bloquear_input()

def editar():
    desbloquear_input()
    nombre=dlg.lista.selectedItems()[1].text()
    apellidos=dlg.lista.selectedItems()[2].text()
    dni=str(dlg.lista.selectedItems()[3].text())
    print(nombre, apellidos,dni)

def salir():
    app.closeAllWindows()

    # Zona asociación funciones
dlg.btn_nuevo.clicked.connect(nuevo)
dlg.input_nombre.textChanged.connect(comprobarGuardar)
dlg.input_apellidos.textChanged.connect(comprobarGuardar)
dlg.input_dni.textChanged.connect(comprobarGuardar)
dlg.btn_guardar.clicked.connect(guardar)
dlg.btn_cancelar.clicked.connect(cancelar)
dlg.lista.clicked.connect(selectTabla)
dlg.btn_eliminar.clicked.connect(eliminar)
dlg.btn_editar.clicked.connect(editar)


dlg.btn_salir.clicked.connect(salir)
conectar()


dlg.show()
app.exec()
