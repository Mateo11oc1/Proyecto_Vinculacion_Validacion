import sys
import tkinter as tk
from PyQt6.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QScreen
from vista.reportes import Ventana
from modelo.validaciones import *

class Controlador(QWidget):

    def __init__(self):

        super().__init__()
        # instancio la ventana
        self.app = QtWidgets.QApplication(sys.argv)
        self.vista = Ventana()
        self.centrarVentana()
        self.tabla = None
        #----------------------
        self.modelo = Validaciones()
        
        #---------------------------------------------------------------------------------
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
        self.vista.ui.tblTablaErrores.setModel(None)
        self.carpeta = QFileDialog.getExistingDirectory(self, "Selecciona una carpeta", "/")
        if self.carpeta and os.path.isdir(self.carpeta):
            self.modelo.leerCarpeta(self.carpeta)
            mensaje=QMessageBox()
            mensaje.setText("Cargando datos... Por favor no cierre la ventana principal")
            mensaje.exec()
            columnasConErrores, columnasConCorrecciones, hojas_mal_formato = self.modelo.leerColumna(1)
            self.llenarTablaErrores(columnasConErrores)
            self.llenarTablaCorrecciones(columnasConCorrecciones)
            self.llenarTablaMalFormato(hojas_mal_formato)
            

    def llenarTablaErrores(self, columnasConErrores):
        self.setCabecerasTablaErrores()
    
        
        for i in range(len(columnasConErrores)):
            self.tabla.setItem(i,0,QStandardItem(str(columnasConErrores[i]["archivoNombre"])))
            self.tabla.setItem(i,1,QStandardItem(str(columnasConErrores[i]["nombreHoja"])))
            self.tabla.setItem(i,2,QStandardItem(str(columnasConErrores[i]["numColumna"])))
            self.tabla.setItem(i,3,QStandardItem(str(columnasConErrores[i]["atractor"])))
            self.tabla.setItem(i,4,QStandardItem(str(self.detalleErrores(columnasConErrores[i]["listaErrores"]))))
            self.tabla.setItem(i,5,QStandardItem(str(columnasConErrores[i]["tramo"])))
            self.tabla.setItem(i,6,QStandardItem(str(columnasConErrores[i]["zona"])))
            self.tabla.setItem(i,7,QStandardItem(str(columnasConErrores[i]["grupo"])))


        self.vista.ui.tblTablaErrores.resizeColumnsToContents()
        self.vista.ui.tblTablaErrores.resizeRowsToContents()

    def llenarTablaCorrecciones(self, columnasConCorrecciones):
        self.setCabecerasTablaCorrecciones()
    
        
        for i in range(len(columnasConCorrecciones)):
            self.tablaCorreccion.setItem(i,0,QStandardItem(str(columnasConCorrecciones[i]["archivoNombre"])))
            self.tablaCorreccion.setItem(i,1,QStandardItem(str(columnasConCorrecciones[i]["nombreHoja"])))
            self.tablaCorreccion.setItem(i,2,QStandardItem(str(columnasConCorrecciones[i]["atractor"])))
            self.tablaCorreccion.setItem(i,3,QStandardItem(str(self.detalleCorrecciones(columnasConCorrecciones[i]["listaCorrecciones"]))))
            self.tablaCorreccion.setItem(i,4,QStandardItem(str(columnasConCorrecciones[i]["tramo"])))
            self.tablaCorreccion.setItem(i,5,QStandardItem(str(columnasConCorrecciones[i]["zona"])))
            self.tablaCorreccion.setItem(i,6,QStandardItem(str(columnasConCorrecciones[i]["grupo"])))


        self.vista.ui.tblTablaCorreciones.resizeColumnsToContents()
        self.vista.ui.tblTablaCorreciones.resizeRowsToContents()

    def llenarTablaMalFormato(self, malformato):
        tablaMalFormato = QStandardItemModel()
        tablaMalFormato.setHorizontalHeaderLabels(["Nombre archivo", "Nombre de hoja"])
        self.vista.ui.tblFormatoIncorrecto.setModel(tablaMalFormato)
        cabecera = self.vista.ui.tblFormatoIncorrecto.horizontalHeader()
        cabecera.resizeSection(0,450)
        cabecera.resizeSection(1,250)

        for i in range(len(malformato)):
            tablaMalFormato.setItem(i,0,QStandardItem(str(malformato[i]["nombre_archivo"])))
            tablaMalFormato.setItem(i,1,QStandardItem(str(malformato[i]["nombre_hoja"])))


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

    def detalleCorrecciones(self, listaCorrecciones):
        mensajeCorrecciones=""

        if listaCorrecciones[1]==True:
            mensajeCorrecciones+= "Se ha escrito el número de atractores en #Atractores\n"

        if listaCorrecciones[2]==True:
            mensajeCorrecciones+= "Se ha cambiado los datos de #vespertino y #matutino por #diurno\n"

        if listaCorrecciones[3]==True:
            mensajeCorrecciones=mensajeCorrecciones+"Se ha cambiado #lunes, #martes, #miercoles, #jueves, #viernes por #entre semana\n"

        if listaCorrecciones[4]==True:
            mensajeCorrecciones=mensajeCorrecciones+"Se ha modificado el número de atractores en el motivo Vivienda ya que se encontraba en filas inferiores"

        return mensajeCorrecciones

    def setCabecerasTablaErrores(self):
        self.tabla = QStandardItemModel()
        self.tabla.setHorizontalHeaderLabels(["Nombre archivo", "Nombre de hoja", "Numero de columna", "Atractor", "Errores encontrados", "Tramo", "Zona", "Grupo"])
        self.vista.ui.tblTablaErrores.setModel(self.tabla)
        cabecera = self.vista.ui.tblTablaErrores.horizontalHeader()
        # cabecera.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        cabecera.resizeSection(0,120)
        cabecera.resizeSection(1,120)
        cabecera.resizeSection(2,100)
        cabecera.resizeSection(3,660)
        cabecera.resizeSection(4,70)
        cabecera.resizeSection(5,70)
        cabecera.resizeSection(6,70)
    
    def setCabecerasTablaCorrecciones(self):
        self.tablaCorreccion = QStandardItemModel()
        self.tablaCorreccion.setHorizontalHeaderLabels(["Nombre archivo", "Nombre de hoja",  "Atractor", "Correcciones", "Tramo", "Zona", "Grupo"])
        self.vista.ui.tblTablaCorreciones.setModel(self.tablaCorreccion)
        cabecera = self.vista.ui.tblTablaCorreciones.horizontalHeader()
        # cabecera.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        cabecera.resizeSection(0,120)
        cabecera.resizeSection(1,120)
        cabecera.resizeSection(2,100)
        cabecera.resizeSection(3,660)
        cabecera.resizeSection(4,70)
        cabecera.resizeSection(5,70)
        cabecera.resizeSection(6,70)



    def verObservaciones(self):
        self.vista.ui.tblVerObservaciones.setModel(None)
        self.tablaObservaciones = QStandardItemModel()
        self.carpetaObservaciones= QFileDialog.getExistingDirectory(self, "Selecciona una carpeta", "/")

        if self.carpetaObservaciones and os.path.isdir(self.carpetaObservaciones):
            
            self.modelo.leerCarpeta(self.carpetaObservaciones)
            #mensaje=QMessageBox()
            #mensaje.setText("Cargando datos... Por favor no cierre la ventana principal")
            #mensaje.exec()
            archivos = self.modelo.verObservacionesArchivos()
            self.tablaObservaciones.setHorizontalHeaderLabels(["Nombre archivo", "Nombre de hoja",  "Observaciones", "Tramo", "Zona", "Grupo"])
            self.vista.ui.tblVerObservaciones.setModel(self.tablaObservaciones)

            for i in range(len(archivos)):
                self.tablaObservaciones.setItem(i,0,QStandardItem(str(archivos[i]["archivoNombre"])))
                self.tablaObservaciones.setItem(i,1,QStandardItem(str(archivos[i]["nombreHoja"])))
                self.tablaObservaciones.setItem(i,2,QStandardItem(str(archivos[i]["observaciones"])))
                self.tablaObservaciones.setItem(i,3,QStandardItem(str(archivos[i]["tramo"])))
                self.tablaObservaciones.setItem(i,4,QStandardItem(str(archivos[i]["zona"])))
                self.tablaObservaciones.setItem(i,5,QStandardItem(str(archivos[i]["grupo"])))

            self.vista.ui.tblVerObservaciones.resizeColumnsToContents()
            self.vista.ui.tblVerObservaciones.resizeRowsToContents()

    def seleccionarArchivo(self):
        self.vista.ui.tblTablaErrores.setModel(None)
        self.archivo, ok = QFileDialog.getOpenFileName(self, "Seleccionar archivo", r"<Default dir>", "Archivos excel (*.xlsx)")
        if ok:
            
            self.setCabecerasTablaErrores()
            self.modelo.archivos_excel = [self.archivo]
            columnasConErrores, columnasConCorrecciones, hojas_mal_formato = self.modelo.leerColumna(2)
            self.llenarTablaErrores(columnasConErrores)
            self.llenarTablaCorrecciones(columnasConCorrecciones)
            self.llenarTablaMalFormato(hojas_mal_formato)
        
