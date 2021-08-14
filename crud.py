# sqlite > CREATE TABLE personas(
#   ... > id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#   ... > nombre TEXT NOT NULL,
#   ... > apellidos TEXT NOT NULL,
#   ... > dni TEXT NOT NULL);


from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sqlite3

app = QtWidgets.QApplication([])
dlg = uic.loadUi('crud.ui')

editarONuevo = True  # variable general para saber si se esta actualizando o es uno nuevo
# Zona funciones

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
    dni = dni.upper().strip()
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
    global editarONuevo
    desbloquear_input()
    dlg.btn_cancelar.setDisabled(False)
    editarONuevo = True
    dlg.input_buscar.setText('')


def borrarTabla():
    while dlg.lista.rowCount() > 0:
        dlg.lista.removeRow(0)


def refresh():
    borrarTabla()
    conectar()


def cancelar():
    dlg.input_nombre.setText('')
    dlg.input_apellidos.setText('')
    dlg.input_dni.setText('')
    bloquear_input()
    dlg.btn_cancelar.setDisabled(True)
    dlg.btn_eliminar.setDisabled(True)
    dlg.btn_nuevo.setDisabled(False)
    dlg.btn_editar.setDisabled(True)
    dlg.input_buscar.setText('')


def selectTabla():
    dlg.btn_eliminar.setDisabled(False)
    dlg.btn_nuevo.setDisabled(True)
    dlg.btn_cancelar.setDisabled(False)
    bloquear_input()
    dlg.btn_editar.setDisabled(False)


def eliminar():
    con = sqlite3.connect('personas.db')
    cursor = con.cursor()
    query = "DELETE FROM personas where ID='"+str(dlg.lista.selectedItems()[0].text())+"'"
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
    dlg.btn_editar.setDisabled(True)
    dlg.input_buscar.setText('')


def guardar():
    global editarONuevo
    con = sqlite3.connect('personas.db')
    cursor = con.cursor()
    nombre = dlg.input_nombre.text().strip()
    apellidos = dlg.input_apellidos.text().strip()
    dni = dlg.input_dni.text().upper().strip()
    print(editarONuevo)
    if editarONuevo == True:
        query = "INSERT INTO personas (nombre,apellidos,dni) VALUES ('" + \
            nombre + "','" + apellidos + "','" + dni + "')"
    elif editarONuevo == False:
        query = "UPDATE personas SET nombre='"+nombre + \
            "',apellidos='"+apellidos+"',dni='"+dni+"' WHERE ID='"+str(dlg.lista.selectedItems()[0].text())+"'"
        dlg.btn_nuevo.setDisabled(False)
    cursor.execute(query)
    con.commit()
    cursor.close()
    refresh()
    dlg.input_nombre.setText('')
    dlg.input_apellidos.setText('')
    dlg.input_dni.setText('')
    bloquear_input()
    dlg.btn_cancelar.setDisabled(True)
    dlg.btn_editar.setDisabled(True)
    dlg.input_buscar.setText('')


def editar():
    global editarONuevo
    editarONuevo = False
    desbloquear_input()
    nombre = dlg.lista.selectedItems()[1].text()
    apellidos = dlg.lista.selectedItems()[2].text()
    dni = str(dlg.lista.selectedItems()[3].text())
    dlg.input_nombre.setText(nombre)
    dlg.input_apellidos.setText(apellidos)
    dlg.input_dni.setText(dni)
    dlg.btn_eliminar.setDisabled(True)
    dlg.btn_editar.setDisabled(True)
    dlg.input_buscar.setText('')


def buscar():
    palabra = dlg.input_buscar.text()
    if len(palabra) > 2:
        con = sqlite3.connect('personas.db')
        cursor = con.cursor()
        #query="SELECT * FROM personas WHERE nombre LIKE '%"+palabra+"%' OR apellidos LIKE '%"+palabra+"%' OR dni LIKE '%"+palabra+"%'"
        query="Select * from personas where replace(replace(replace(replace(replace(nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u') like '%"+palabra+"%' or replace(replace(replace(replace(replace(apellidos,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u') like '%"+palabra+"%' or dni LIKE '%"+palabra+"%'"
        result=cursor.execute(query)
        if result:
            borrarTabla()
            for num_row, items in enumerate(result):
                print(items)
                dlg.lista.insertRow(num_row)
                for num_col, dato in enumerate(items):
                    cell = QtWidgets.QTableWidgetItem(str(dato))
                    cell.setTextAlignment(QtCore.Qt.AlignCenter)
                    dlg.lista.setItem(num_row, num_col, cell)
        cursor.close()
    elif len(palabra)<3: refresh()


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
dlg.input_buscar.textChanged.connect(buscar)

dlg.btn_salir.clicked.connect(salir)
conectar()

dlg.setWindowTitle('Base de datos de usuarios en SQLite3') # Nombre del título
dlg.setWindowIcon(QIcon('usuario.png')) # Icono del título

dlg.show()
app.exec()
