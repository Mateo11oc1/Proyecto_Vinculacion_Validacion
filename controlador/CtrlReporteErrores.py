import sys
import tkinter as tk


from PyQt6.QtWidgets import QWidget, QFileDialog, QApplication
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QScreen

# from PyQt6.uic.properties import QtWidgets
from vista.reportes import Ventana
from vista.reportes import LoadingWidget
from modelo.validaciones import *

class Controlador(QWidget):

    def __init__(self):

        super().__init__()
        # instancio la ventana
        self.app = QtWidgets.QApplication(sys.argv)
        self.vista = Ventana()
        self.centrarVentana()
        #----------------------
        self.modelo = Validaciones()
        

        self.vista.ui.btnSeleccionarCarpeta.clicked.connect(self.buscarCarpeta)
        self.vista.ui.btnVerObservaciones.clicked.connect(self.verObservaciones)
        self.vista.ui.btnSeleccionarArchivo.clicked.connect(self.seleccionarArchivo)


    def centrarVentana(self):
        # obtener la geometría de la pantalla
        screen_geometry = QApplication.primaryScreen().geometry()

        # obtener el tamaño de la ventana
        window_size = self.vista.geometry()

        # calcular la posición central de la ventana
        x = int((screen_geometry.width() - window_size.width()) / 2)
        y = int((screen_geometry.height() - window_size.height()) / 2)

        # mover la ventana a la posición central
        self.vista.move(x, y)

    def buscarCarpeta(self):

        self.carpeta = QFileDialog.getExistingDirectory(self, "Selecciona una carpeta", "/")
        if self.carpeta and os.path.isdir(self.carpeta):
            self.setCabeceras()
            self.modelo.leerCarpeta(self.carpeta)

            columnasConErrores = self.modelo.leerColumna('errores')

            # self.loading=LoadingWidget()
            # self.loading.show()

            # for i in range(len(columnasConErrores)):
            #     progress=int(i/(len(columnasConErrores)-1)*100)
            #     self.loading.set_progress(progress)

            for i in range(len(columnasConErrores)):
                self.tabla.setItem(i,0,QStandardItem(str(columnasConErrores[i]["archivoNombre"])))
                self.tabla.setItem(i,1,QStandardItem(str(columnasConErrores[i]["hoja"])))
                self.tabla.setItem(i,2,QStandardItem(str(columnasConErrores[i]["atractor"])))
                self.tabla.setItem(i,3,QStandardItem(str(self.detalleErrores(columnasConErrores[i]["listaErrores"]))))
                self.tabla.setItem(i,4,QStandardItem(str(columnasConErrores[i]["tramo"])))
                self.tabla.setItem(i,5,QStandardItem(str(columnasConErrores[i]["zona"])))
                self.tabla.setItem(i,6,QStandardItem(str(columnasConErrores[i]["grupo"])))


            self.vista.ui.tblTablaErrores.resizeColumnsToContents()
            self.vista.ui.tblTablaErrores.resizeRowsToContents()


    def detalleErrores(self, listaErrores):
        mensajeErrores=""

        if listaErrores[1]:
            mensajeErrores+= "Se han ingresado caracteres\n"

        if listaErrores[2]:
            mensajeErrores+= "Hay datos de numero de atractores, jornada o dias pero los datos del tamanio estan vacios\n"

        if listaErrores[3]:
            mensajeErrores=mensajeErrores+"La suma de los tamanios no coincide con el numero de atractores\n"

        if listaErrores[4]:
            mensajeErrores=mensajeErrores+"Hay datos de numero de atractores, tamanio o dias pero los datos de la jornada estan vacios\n"

        if listaErrores[5]:
            mensajeErrores=mensajeErrores+"La suma de los datos de la jornada es menor al numero de atractores\n"
        if listaErrores[6]:
            mensajeErrores=mensajeErrores+"Hay uno o varios datos de la jornada que sobrepasa el numero de atractores\n"

        if listaErrores[7]:
            mensajeErrores=mensajeErrores + "Hay datos de numero de atractores, tamanio o jornada pero los datos de los dias estan vacios\n"

        if listaErrores[8]:
            mensajeErrores=mensajeErrores+"Uno o varios de los datos de los días de atención sobrepasan el numero de atractores\n"

        if listaErrores[9]:
            mensajeErrores=mensajeErrores+"La suma de los datos de los dias es menor al numero de atractores\n"

        return mensajeErrores


    def setCabeceras(self):
        tabla = QStandardItemModel()
        tabla.setHorizontalHeaderLabels(["Nombre archivo", "Número de hoja", "Atractor", "Detalle", "Tramo", "Zona", "Grupo"])
        self.vista.ui.tblTablaErrores.setModel(tabla)
        cabecera = self.vista.ui.tblTablaErrores.horizontalHeader()
        # cabecera.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        cabecera.resizeSection(0,120)
        cabecera.resizeSection(1,120)
        cabecera.resizeSection(2,100)
        cabecera.resizeSection(3,660)
        cabecera.resizeSection(4,70)
        cabecera.resizeSection(5,70)
        cabecera.resizeSection(6,70)


    def verObservaciones(self):
        tabla = QStandardItemModel()
        self.carpetaObservaciones= QFileDialog.getExistingDirectory(self, "Selecciona una carpeta", "/")
        if self.carpetaObservaciones and os.path.isdir(self.carpetaObservaciones):
            self.modelo.leerCarpeta(self.carpetaObservaciones)

            archivosConObservaciones = self.modelo.leerColumna('observaciones')
            tabla.setHorizontalHeaderLabels(["Nombre archivo", "Número de hoja",  "Observaciones", "Tramo", "Zona", "Grupo"])
            self.vista.ui.tblTablaErrores.setModel(tabla)

            for i in range(len(archivosConObservaciones)):
                tabla.setItem(i,0,QStandardItem(str(archivosConObservaciones[i]["archivoNombre"])))
                tabla.setItem(i,1,QStandardItem(str(archivosConObservaciones[i]["hoja"])))
                tabla.setItem(i,2,QStandardItem(str(archivosConObservaciones[i]["observaciones"])))
                tabla.setItem(i,3,QStandardItem(str(archivosConObservaciones[i]["tramo"])))
                tabla.setItem(i,4,QStandardItem(str(archivosConObservaciones[i]["zona"])))
                tabla.setItem(i,5,QStandardItem(str(archivosConObservacion[i]["grupo"])))

            self.vista.ui.tblTablaErrores.resizeColumnsToContents()
            self.vista.ui.tblTablaErrores.resizeRowsToContents()

    def seleccionarArchivo(self):
        self.archivo, ok = QFileDialog.getOpenFileName(self, "Seleccionar archivo", r"<Default dir>", "Archivos excel (*.xlsx)")

        if ok:

            self.setCabeceras()
            self.modelo.archivos_excel = [self.archivo]
            columnasConErrores = self.modelo.leerColumna('errores')

            for i in range(len(columnasConErrores)):
                self.tabla.setItem(i,0,QStandardItem(columnasConErrores[i]["archivoNombre"]))
                self.tabla.setItem(i,1,QStandardItem(str(columnasConErrores[i]["hoja"])))
                self.tabla.setItem(i,2,QStandardItem(columnasConErrores[i]["atractor"]))
                self.tabla.setItem(i,3,QStandardItem(self.detalleErrores(columnasConErrores[i]["listaErrores"])))
                self.tabla.setItem(i,4,QStandardItem(columnasConErrores[i]["tramo"]))
                self.tabla.setItem(i,5,QStandardItem(str(columnasConErrores[i]["zona"])))
                self.tabla.setItem(i,6,QStandardItem(str(columnasConErrores[i]["grupo"])))


            self.vista.ui.tblTablaErrores.resizeColumnsToContents()
            self.vista.ui.tblTablaErrores.resizeRowsToContents()


