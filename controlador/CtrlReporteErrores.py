import sys
import tkinter as tk
from PyQt6.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QScreen
from vista.reportes import Ventana
from modelo.validaciones import *
import pyttsx3
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
        carpeta = QFileDialog.getExistingDirectory(self, "Selecciona una carpeta", "/")
        if carpeta and os.path.isdir(carpeta):
            self.modelo = Validaciones()
            self.modelo.leerCarpeta(carpeta)
            mensaje=QMessageBox()
            mensaje.setText("Cargando datos... Por favor no cierre esta ventana. Presione 'OK' para comenzar")
            mensaje.exec()
            confirmar="¿Desea que tambien se realice una comprobación de las calles de los archivos?"
            respuesta = QMessageBox.question(self, "Confirmación", confirmar, QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            #si la respuesta es que si
            if respuesta == 16384:
                columnasConErrores, columnasConCorrecciones, hojas_mal_formato, calles_invalidas, zona_grupo_vacias = self.modelo.procesar_archivos_excel(1, True)
                self.llenarTablaCallesMalEscritas(calles_invalidas)
            else:
                columnasConErrores, columnasConCorrecciones, hojas_mal_formato, calles_invalidas, zona_grupo_vacias = self.modelo.procesar_archivos_excel(1, False)


            self.llenarTablaErrores(columnasConErrores)
            self.llenarTablaCorrecciones(columnasConCorrecciones)
            self.llenarTablaMalFormato(hojas_mal_formato)
            
            self.llenarTablaZonaGrupoVacios(zona_grupo_vacias)
            self.avisoPorVoz()

    def llenarTablaErrores(self, columnasConErrores):
        self.setCabecerasTablaErrores()
    
        
        for i in range(len(columnasConErrores)):
            self.tabla.setItem(i,0,QStandardItem(str(columnasConErrores[i]["nombre_archivo"])))
            self.tabla.setItem(i,1,QStandardItem(str(columnasConErrores[i]["nombre_hoja"])))
            self.tabla.setItem(i,2,QStandardItem(str(columnasConErrores[i]["numColumna"])))
            self.tabla.setItem(i,3,QStandardItem(str(columnasConErrores[i]["atractor"])))
            self.tabla.setItem(i,4,QStandardItem(str(self.detalleErrores(columnasConErrores[i]["listaErrores"]))))
            self.tabla.setItem(i,5,QStandardItem(str(columnasConErrores[i]["tramo"])))
            self.tabla.setItem(i,6,QStandardItem(str(columnasConErrores[i]["zona"])))
            self.tabla.setItem(i,7,QStandardItem(str(columnasConErrores[i]["grupo"])))

        if len(columnasConErrores)!=0:
            self.vista.ui.tblTablaErrores.resizeColumnsToContents()
            self.vista.ui.tblTablaErrores.resizeRowsToContents()

    def llenarTablaCorrecciones(self, columnasConCorrecciones):
        self.setCabecerasTablaCorrecciones()
    
        
        for i in range(len(columnasConCorrecciones)):
            self.tablaCorreccion.setItem(i,0,QStandardItem(str(columnasConCorrecciones[i]["nombre_archivo"])))
            self.tablaCorreccion.setItem(i,1,QStandardItem(str(columnasConCorrecciones[i]["nombre_hoja"])))
            self.tablaCorreccion.setItem(i,2,QStandardItem(str(columnasConCorrecciones[i]["atractor"])))
            self.tablaCorreccion.setItem(i,3,QStandardItem(str(self.detalleCorrecciones(columnasConCorrecciones[i]["listaCorrecciones"]))))
            self.tablaCorreccion.setItem(i,4,QStandardItem(str(columnasConCorrecciones[i]["tramo"])))
            self.tablaCorreccion.setItem(i,5,QStandardItem(str(columnasConCorrecciones[i]["zona"])))
            self.tablaCorreccion.setItem(i,6,QStandardItem(str(columnasConCorrecciones[i]["grupo"])))

        if len(columnasConCorrecciones)!=0:
            self.vista.ui.tblTablaCorreciones.resizeRowsToContents()
            self.vista.ui.tblTablaCorreciones.resizeColumnsToContents()


    def llenarTablaMalFormato(self, malformato):
        tablaMalFormato = QStandardItemModel()
        tablaMalFormato.setHorizontalHeaderLabels(["Nombre archivo", "Nombre de hoja"])
        self.vista.ui.tblFormatoIncorrecto_2.setModel(tablaMalFormato)
        cabecera = self.vista.ui.tblFormatoIncorrecto_2.horizontalHeader()
        cabecera.resizeSection(0,450)
        cabecera.resizeSection(1,250)

        for i in range(len(malformato)):
            tablaMalFormato.setItem(i,0,QStandardItem(str(malformato[i]["nombre_archivo"])))
            tablaMalFormato.setItem(i,1,QStandardItem(str(malformato[i]["nombre_hoja"])))

    def llenarTablaCallesMalEscritas(self, calles):
        tablaCalles = QStandardItemModel()
        tablaCalles.setHorizontalHeaderLabels(["Nombre archivo", "Nombre de hoja", "Calle no reconocida", "Tipo de calle"])
        self.vista.ui.tblCallesNoReconocidas.setModel(tablaCalles)
        cabecera = self.vista.ui.tblCallesNoReconocidas.horizontalHeader()
        cabecera.resizeSection(0,450)
        cabecera.resizeSection(1,200)
        cabecera.resizeSection(2,500)
        cabecera.resizeSection(3,131)

        for i in range(len(calles)):
            tablaCalles.setItem(i,0,QStandardItem(str(calles[i]["nombre_archivo"])))
            tablaCalles.setItem(i,1,QStandardItem(str(calles[i]["nombre_hoja"])))
            tablaCalles.setItem(i,2,QStandardItem(str(calles[i]["calle"])))
            tablaCalles.setItem(i,3,QStandardItem(str(calles[i]["tipo"])))
        
        if len(calles)!=0:
            self.vista.ui.tblCallesNoReconocidas.resizeColumnsToContents()
            self.vista.ui.tblCallesNoReconocidas.resizeRowsToContents()
        
    def llenarTablaZonaGrupoVacios(self, hojas):
        tablaZonaGrupo = QStandardItemModel()
        tablaZonaGrupo.setHorizontalHeaderLabels(["Nombre archivo", "Nombre de hoja", "Errores", "Zona", "Grupo"])
        self.vista.ui.tblZonaOGrupoVacios.setModel(tablaZonaGrupo)
        cabecera = self.vista.ui.tblZonaOGrupoVacios.horizontalHeader()
        cabecera.resizeSection(0,300)
        cabecera.resizeSection(1,200)
        cabecera.resizeSection(2,600)
        cabecera.resizeSection(3,100)
        cabecera.resizeSection(4,100)
        

        for i in range(len(hojas)):
            tablaZonaGrupo.setItem(i,0,QStandardItem(str(hojas[i]["nombre_archivo"])))
            tablaZonaGrupo.setItem(i,1,QStandardItem(str(hojas[i]["nombre_hoja"])))
            tablaZonaGrupo.setItem(i,2,QStandardItem(str(hojas[i]["errores"])))
            tablaZonaGrupo.setItem(i,3,QStandardItem(str(hojas[i]["zona"])))
            tablaZonaGrupo.setItem(i,4,QStandardItem(str(hojas[i]["grupo"])))
        
        if len(hojas)!=0:
            self.vista.ui.tblZonaOGrupoVacios.resizeColumnsToContents()
            self.vista.ui.tblZonaOGrupoVacios.resizeRowsToContents()


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
        cabecera.resizeSection(3,560)
        cabecera.resizeSection(4,70)
        cabecera.resizeSection(5,70)
        cabecera.resizeSection(6,70)



    def verObservaciones(self):
        self.vista.ui.tblVerObservaciones.setModel(None)
        tablaObservaciones = QStandardItemModel()
        carpetaObservaciones= QFileDialog.getExistingDirectory(self, "Selecciona una carpeta", "/")

        if carpetaObservaciones and os.path.isdir(carpetaObservaciones):
            self.modelo = Validaciones()
            self.modelo.leerCarpeta(carpetaObservaciones)
            #mensaje=QMessageBox()
            #mensaje.setText("Cargando datos... Por favor no cierre la ventana principal")
            #mensaje.exec()
            archivos = self.modelo.verObservacionesArchivos()
            tablaObservaciones.setHorizontalHeaderLabels(["Nombre archivo", "Nombre de hoja",  "Observaciones", "Tramo", "Zona", "Grupo"])
            self.vista.ui.tblVerObservaciones.setModel(tablaObservaciones)

            for i in range(len(archivos)):
                tablaObservaciones.setItem(i,0,QStandardItem(str(archivos[i]["nombre_archivo"])))
                tablaObservaciones.setItem(i,1,QStandardItem(str(archivos[i]["nombre_hoja"])))
                tablaObservaciones.setItem(i,2,QStandardItem(str(archivos[i]["observaciones"])))
                tablaObservaciones.setItem(i,3,QStandardItem(str(archivos[i]["tramo"])))
                tablaObservaciones.setItem(i,4,QStandardItem(str(archivos[i]["zona"])))
                tablaObservaciones.setItem(i,5,QStandardItem(str(archivos[i]["grupo"])))

            self.vista.ui.tblVerObservaciones.resizeColumnsToContents()
            self.vista.ui.tblVerObservaciones.resizeRowsToContents()

    def seleccionarArchivo(self):
        self.vista.ui.tblTablaErrores.setModel(None)
        archivo, ok = QFileDialog.getOpenFileName(self, "Seleccionar archivo", r"<Default dir>", "Archivos excel (*.xlsx)")
        if ok:
            self.modelo = Validaciones()
            self.setCabecerasTablaErrores()
            self.modelo.archivos_excel = [archivo]
            confirmar="¿Desea que tambien se realice una comprobación de las calles de los archivos?"
            respuesta = QMessageBox.question(self, "Confirmación", confirmar, QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            #si la respuesta es que si
            if respuesta == 16384:
                columnasConErrores, columnasConCorrecciones, hojas_mal_formato, calles_invalidas, zona_grupo_vacias = self.modelo.procesar_archivos_excel(2, True)
                self.llenarTablaCallesMalEscritas(calles_invalidas)
            else:
                columnasConErrores, columnasConCorrecciones, hojas_mal_formato, calles_invalidas, zona_grupo_vacias = self.modelo.procesar_archivos_excel(2, False)

            self.llenarTablaErrores(columnasConErrores)
            self.llenarTablaCorrecciones(columnasConCorrecciones)
            self.llenarTablaMalFormato(hojas_mal_formato)
            self.llenarTablaZonaGrupoVacios(zona_grupo_vacias)
            self.avisoPorVoz()
        
    def avisoPorVoz(self):
        voz = pyttsx3.init()
        voz.setProperty('rate', 150)
        mensaje = "El programa ha terminado su ejecución. Revise las pestañas de la interfaz para observar los resultados"
        voz.say(mensaje)
        voz.runAndWait()