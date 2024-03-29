# sqlite > CREATE TABLE personas(
#   ... > id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#   ... > nombre TEXT NOT NULL,
#   ... > apellidos TEXT NOT NULL,
#   ... > dni TEXT NOT NULL);


import sqlite3

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
        # print(items)
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


def nuevoDNI(dni):
    global editarONuevo
    # print('editar o guardar', editarONuevo)
    nuevo = True
    # print('dni: ', dni)
    num_rows = dlg.lista.rowCount()
    if editarONuevo: # guardar
        for i in range(0, num_rows):
            value = dlg.lista.item(i, 3)
            value = value.text()
            # print(i,': ',dni.upper(), value)
            if dni.upper() == value:
                nuevo = False
                break
    else: # editar
        for i in range(0, num_rows):
            value = dlg.lista.item(i, 3)
            value = value.text()
            # print(i,': ',dni.upper(), value)
            if dni.upper() == value != str(dlg.lista.selectedItems()[3].text()):
                nuevo = False
                break
    return nuevo

def validoNombre(nombre):
    if len(nombre) > 2 and nombre.isalpha():
        # print('nombre válido')
        return True
    else:
        # print('no válido')
        return False
        

def comprobarGuardar():
    if validoNombre(dlg.input_nombre.text()) and validoNombre(dlg.input_apellidos.text()) and validoDNI(dlg.input_dni.text()) and nuevoDNI(dlg.input_dni.text()):
        dlg.btn_guardar.setDisabled(False)
        dlg.lbl_mensaje_dni.setText('')
    else:
        dlg.btn_guardar.setDisabled(True)
        if validoNombre(dlg.input_nombre.text()) == False:
            dlg.lbl_mensaje_nombre.setText('Nombre no válido')
        if len(dlg.input_nombre.text()) == 0 or validoNombre(dlg.input_nombre.text()) == True:
            dlg.lbl_mensaje_nombre.setText('')

        if validoNombre(dlg.input_apellidos.text()) == False:
            dlg.lbl_mensaje_apellidos.setText('Apellidos no válidos')
        if len(dlg.input_apellidos.text()) == 0 or validoNombre(dlg.input_apellidos.text()) == True:
            dlg.lbl_mensaje_apellidos.setText('')

        if validoDNI(dlg.input_dni.text()) == False:
            dlg.lbl_mensaje_dni.setText('Dni no válido')
        if nuevoDNI(dlg.input_dni.text()) == False:
            dlg.lbl_mensaje_dni.setText('Dni existente en la bd')
        if len(dlg.input_dni.text()) == 0 or (validoDNI(dlg.input_dni.text()) == True and nuevoDNI(dlg.input_dni.text()) == True):
            dlg.lbl_mensaje_dni.setText('')
        
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
    query = "DELETE FROM personas where ID='" + \
        str(dlg.lista.selectedItems()[0].text())+"'"
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Acción peligrosa")
    msg.setInformativeText("¿Esta segur@ de que desea eliminar la fila?")
    msg.setWindowTitle("Aviso")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.addButton(QMessageBox.No)
    respuesta = msg.exec_()
    if respuesta == QMessageBox.Ok:
        # print('Borra')
        cursor.execute(query)
        con.commit()
        cursor.close()
        refresh()
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
    # print(editarONuevo)
    if editarONuevo == True:
        query = "INSERT INTO personas (nombre,apellidos,dni) VALUES ('" + \
            nombre + "','" + apellidos + "','" + dni + "')"
    elif editarONuevo == False:
        query = "UPDATE personas SET nombre='"+nombre + \
            "',apellidos='"+apellidos+"',dni='"+dni+"' WHERE ID='" + \
                str(dlg.lista.selectedItems()[0].text())+"'"
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
        # query="SELECT * FROM personas WHERE nombre LIKE '%"+palabra+"%' OR apellidos LIKE '%"+palabra+"%' OR dni LIKE '%"+palabra+"%'"
        query = "Select * from personas where replace(replace(replace(replace(replace(nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u') like '%"+palabra + \
            "%' or replace(replace(replace(replace(replace(apellidos,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u') like '%" + \
            palabra+"%' or dni LIKE '%"+palabra+"%'"
        result = cursor.execute(query)
        if result:
            borrarTabla()
            for num_row, items in enumerate(result):
                # print(items)
                dlg.lista.insertRow(num_row)
                for num_col, dato in enumerate(items):
                    cell = QtWidgets.QTableWidgetItem(str(dato))
                    cell.setTextAlignment(QtCore.Qt.AlignCenter)
                    dlg.lista.setItem(num_row, num_col, cell)
        cursor.close()
    elif len(palabra) < 3:
        refresh()


def salir():
    app.closeAllWindows()


def minimiza():
    dlg.hide()
    menu.removeAction(quitAction)
    menu.addAction(maximizeAction)
    menu.addAction(quitAction)
    menu.removeAction(minimizeAction)


def maximiza():
    dlg.show()
    menu.removeAction(quitAction)
    menu.addAction(minimizeAction)
    menu.addAction(quitAction)
    menu.removeAction(maximizeAction)


# Icono en el tray
trayIcon = QSystemTrayIcon(QIcon('usuario.png'), parent=app)
trayIcon.setToolTip('Base de Datos SQLite3')


def icono():
    if dlg.checkIcono.isChecked():
        trayIcon.show()
    else:
        trayIcon.hide()

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
dlg.checkIcono.clicked.connect(icono)
conectar()

# Barra del título
dlg.setWindowTitle('Base de datos de usuarios en SQLite3')  # Nombre del título
dlg.setWindowIcon(QIcon('usuario.png'))  # Icono del título

# Opciones de minimizar/maximizar y salir al icono del tray
menu = QMenu()
minimizeAction = menu.addAction('Minimizar')
minimizeAction.triggered.connect(minimiza)
quitAction = menu.addAction('Cerrar')
quitAction.triggered.connect(dlg.close)
trayIcon.setContextMenu(menu)  # Aquí se añaden al icono
maximizeAction = menu.addAction('Maximizar')
maximizeAction.triggered.connect(maximiza)
menu.removeAction(maximizeAction)  # Una vez creada se elimina del icono

# Minimizar/maximizar con doble click


def onTrayIconActivated(reason):
    if reason == trayIcon.DoubleClick:
        # print('double click')
        if dlg.isVisible():
            minimiza()
        else:
            maximiza()


trayIcon.activated.connect(onTrayIconActivated)

# Centrar ventana
qr = dlg.frameGeometry()
cp = QtWidgets.QDesktopWidget().availableGeometry().center()
qr.moveCenter(cp)
dlg.move(qr.topLeft())

dlg.show()
app.exec()
