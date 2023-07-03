# Form implementation generated from reading ui file 'reportes-errores.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 820)
        MainWindow.setStyleSheet(".QPushButton{\n"
"    color: rgb(0, 0, 127);\n"
"    background-color: rgb(255,255,255);\n"
"    border-radius:15;\n"
"\n"
"}\n"
".QPushButton:hover{\n"
"    background-color:#c4c4c4;\n"
"    color:black;\n"
"}\n"
"\n"
"[name = fondoErrores]{\n"
"    background-image: url(\"C:\\Users\\aimbe\\Downloads\\Recurso 6-100\\\")\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 1310, 820))
        self.tab_widget.setObjectName("tab_widget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setGeometry(QtCore.QRect(-230, -290, 1531, 1101))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(230, 290, 1301, 791))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("./imagenes/Recurso 6-100.jpg"))
        self.label_5.setObjectName("label_5")
        self.btnSeleccionarCarpeta = QtWidgets.QPushButton(self.frame)
        self.btnSeleccionarCarpeta.setGeometry(QtCore.QRect(930, 400, 211, 61))
        self.btnSeleccionarCarpeta.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./imagenes/seleccionar-carpteta.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnSeleccionarCarpeta.setIcon(icon)
        self.btnSeleccionarCarpeta.setIconSize(QtCore.QSize(50, 50))
        self.btnSeleccionarCarpeta.setObjectName("btnSeleccionarCarpeta")
        self.btnSeleccionarArchivo = QtWidgets.QPushButton(self.frame)
        self.btnSeleccionarArchivo.setGeometry(QtCore.QRect(500, 400, 211, 61))
        self.btnSeleccionarArchivo.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./imagenes/archivos.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnSeleccionarArchivo.setIcon(icon1)
        self.btnSeleccionarArchivo.setIconSize(QtCore.QSize(50, 50))
        self.btnSeleccionarArchivo.setObjectName("btnSeleccionarArchivo")
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setGeometry(QtCore.QRect(450, 310, 821, 71))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_17.setObjectName("label_17")
        self.textAreaIndicaciones = QtWidgets.QTextEdit(self.frame)
        self.textAreaIndicaciones.setGeometry(QtCore.QRect(280, 500, 1191, 521))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(11)
        self.textAreaIndicaciones.setFont(font)
        self.textAreaIndicaciones.setMouseTracking(False)
        self.textAreaIndicaciones.setStyleSheet("background-color: rgb(255,255,255);\n"
"border-radius:15;\n"
"")
        self.textAreaIndicaciones.setObjectName("textAreaIndicaciones")
        self.textAreaIndicaciones.setEnabled(False)
        self.tab_widget.addTab(self.tab, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.frame_2 = QtWidgets.QFrame(self.tab_4)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 1301, 801))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(0, 0, 1301, 791))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("./imagenes/Recurso 6-100.jpg"))
        self.label_8.setObjectName("label_8")
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setGeometry(QtCore.QRect(240, 20, 821, 71))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setGeometry(QtCore.QRect(40, 10, 631, 291))
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap("./imagenes/carro.png"))
        self.label_12.setObjectName("label_12")
        self.label_15 = QtWidgets.QLabel(self.frame_2)
        self.label_15.setGeometry(QtCore.QRect(790, 460, 451, 311))
        self.label_15.setText("")
        self.label_15.setPixmap(QtGui.QPixmap("./imagenes/moto.png"))
        self.label_15.setObjectName("label_15")
        self.tblFormatoIncorrecto_2 = QtWidgets.QTableView(self.frame_2)
        self.tblFormatoIncorrecto_2.setGeometry(QtCore.QRect(230, 100, 771, 591))
        self.tblFormatoIncorrecto_2.setStyleSheet("background-color: rgb(255,255,255);\n"
"border-radius:15;\n"
"")
        self.tblFormatoIncorrecto_2.setObjectName("tblFormatoIncorrecto_2")
        self.tab_widget.addTab(self.tab_4, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.fondoErrores = QtWidgets.QFrame(self.tab_2)
        self.fondoErrores.setGeometry(QtCore.QRect(0, 0, 1311, 791))
        self.fondoErrores.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.fondoErrores.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.fondoErrores.setObjectName("fondoErrores")
        self.label = QtWidgets.QLabel(self.fondoErrores)
        self.label.setGeometry(QtCore.QRect(0, 0, 1310, 820))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./imagenes/Recurso 6-100.jpg"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.fondoErrores)
        self.label_2.setGeometry(QtCore.QRect(50, 30, 631, 291))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./imagenes/carro.png"))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.fondoErrores)
        self.label_3.setGeometry(QtCore.QRect(1040, 450, 451, 311))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("./imagenes/moto.png"))
        self.label_3.setObjectName("label_3")
        self.tblTablaErrores = QtWidgets.QTableView(self.fondoErrores)
        self.tblTablaErrores.setGeometry(QtCore.QRect(60, 100, 1201, 631))
        self.tblTablaErrores.setStyleSheet("background-color: rgb(255,255,255);\n"
"border-radius:15;\n"
"\n"
"")
        self.tblTablaErrores.setObjectName("tblTablaErrores")
        self.label_4 = QtWidgets.QLabel(self.fondoErrores)
        self.label_4.setGeometry(QtCore.QRect(370, 30, 471, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.lblArchivos = QtWidgets.QLabel(self.fondoErrores)
        self.lblArchivos.setEnabled(True)
        self.lblArchivos.setGeometry(QtCore.QRect(100, 320, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblArchivos.setFont(font)
        self.lblArchivos.setText("")
        self.lblArchivos.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblArchivos.setObjectName("lblArchivos")
        self.label_6 = QtWidgets.QLabel(self.fondoErrores)
        self.label_6.setGeometry(QtCore.QRect(670, 780, 231, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.fondoErrores)
        self.label_7.setGeometry(QtCore.QRect(620, 780, 231, 21))
        self.label_7.setObjectName("label_7")
        self.label.raise_()
        self.label_3.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.tblTablaErrores.raise_()
        self.lblArchivos.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.tab_widget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.frame_3 = QtWidgets.QFrame(self.tab_3)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 1301, 791))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(0, 0, 1301, 801))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap("./imagenes/Recurso 6-100.jpg"))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(400, 30, 581, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_10.setObjectName("label_10")
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(20, 20, 631, 291))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap("./imagenes/carro.png"))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.frame_3)
        self.label_14.setGeometry(QtCore.QRect(840, 440, 451, 311))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap("./imagenes/moto.png"))
        self.label_14.setObjectName("label_14")
        self.tblTablaCorreciones = QtWidgets.QTableView(self.frame_3)
        self.tblTablaCorreciones.setGeometry(QtCore.QRect(60, 130, 1181, 591))
        self.tblTablaCorreciones.setStyleSheet("background-color: rgb(255,255,255);\n"
"border-radius:15;\n"
"")
        self.tblTablaCorreciones.setObjectName("tblTablaCorreciones")
        self.tab_widget.addTab(self.tab_3, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.frame_5 = QtWidgets.QFrame(self.tab_6)
        self.frame_5.setGeometry(QtCore.QRect(0, 0, 1301, 791))
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.label_18 = QtWidgets.QLabel(self.frame_5)
        self.label_18.setGeometry(QtCore.QRect(0, 0, 1291, 791))
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("./imagenes/Recurso 6-100.jpg"))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.frame_5)
        self.label_19.setGeometry(QtCore.QRect(410, 20, 581, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_19.setObjectName("label_19")
        self.tblCallesNoReconocidas = QtWidgets.QTableView(self.frame_5)
        self.tblCallesNoReconocidas.setGeometry(QtCore.QRect(50, 90, 1181, 591))
        self.tblCallesNoReconocidas.setStyleSheet("background-color: rgb(255,255,255);\n"
"border-radius:15;\n"
"")
        self.tblCallesNoReconocidas.setObjectName("tblCallesNoReconocidas")
        self.tab_widget.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.frame_6 = QtWidgets.QFrame(self.tab_7)
        self.frame_6.setGeometry(QtCore.QRect(0, 0, 1301, 801))
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.label_20 = QtWidgets.QLabel(self.frame_6)
        self.label_20.setGeometry(QtCore.QRect(0, 0, 1301, 791))
        self.label_20.setText("")
        self.label_20.setPixmap(QtGui.QPixmap("./imagenes/Recurso 6-100.jpg"))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.frame_6)
        self.label_21.setGeometry(QtCore.QRect(-50, -30, 631, 381))
        self.label_21.setText("")
        self.label_21.setPixmap(QtGui.QPixmap("./imagenes/carro.png"))
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.frame_6)
        self.label_22.setGeometry(QtCore.QRect(800, 480, 491, 291))
        self.label_22.setText("")
        self.label_22.setPixmap(QtGui.QPixmap("./imagenes/moto.png"))
        self.label_22.setObjectName("label_22")
        self.tblZonaOGrupoVacios = QtWidgets.QTableView(self.frame_6)
        self.tblZonaOGrupoVacios.setGeometry(QtCore.QRect(60, 130, 1181, 591))
        self.tblZonaOGrupoVacios.setStyleSheet("background-color: rgb(255,255,255);\n"
"border-radius:15;\n"
"")
        self.tblZonaOGrupoVacios.setObjectName("tblZonaOGrupoVacios")
        self.label_23 = QtWidgets.QLabel(self.frame_6)
        self.label_23.setGeometry(QtCore.QRect(410, 40, 581, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_23.setObjectName("label_23")
        self.tab_widget.addTab(self.tab_7, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.frame_4 = QtWidgets.QFrame(self.tab_5)
        self.frame_4.setGeometry(QtCore.QRect(0, 0, 1301, 791))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_16 = QtWidgets.QLabel(self.frame_4)
        self.label_16.setGeometry(QtCore.QRect(0, 0, 1301, 791))
        self.label_16.setText("")
        self.label_16.setPixmap(QtGui.QPixmap("./imagenes/Recurso 6-100.jpg"))
        self.label_16.setObjectName("label_16")
        self.btnVerObservaciones = QtWidgets.QPushButton(self.frame_4)
        self.btnVerObservaciones.setGeometry(QtCore.QRect(490, 50, 211, 61))
        self.btnVerObservaciones.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./imagenes/ver-observaciones.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnVerObservaciones.setIcon(icon2)
        self.btnVerObservaciones.setIconSize(QtCore.QSize(50, 50))
        self.btnVerObservaciones.setObjectName("btnVerObservaciones")
        self.tblVerObservaciones = QtWidgets.QTableView(self.frame_4)
        self.tblVerObservaciones.setGeometry(QtCore.QRect(40, 140, 1181, 591))
        self.tblVerObservaciones.setStyleSheet("background-color: rgb(255,255,255);\n"
"border-radius:15;\n"
"")
        self.tblVerObservaciones.setObjectName("tblVerObservaciones")
        self.tab_widget.addTab(self.tab_5, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnSeleccionarCarpeta.setToolTip(_translate("MainWindow", "Seleccione una carpeta que contenga archivos excel para validarlos"))
        self.btnSeleccionarCarpeta.setText(_translate("MainWindow", "Seleccionar carpeta"))
        self.btnSeleccionarArchivo.setToolTip(_translate("MainWindow", "Seleccione un solo archivo excel que desee validar, en la tabla se presentará un resumen de los errores"))
        self.btnSeleccionarArchivo.setText(_translate("MainWindow", "Seleccionar archivo"))
        self.label_17.setText(_translate("MainWindow", "VALIDACIÓN Y VERIFICACIÓN DE DATOS"))
        self.textAreaIndicaciones.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cambria\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Para validar los datos de los Formularios Excel, usted tiene dos opciones: seleccionar un archivo específico o seleccionar la carpeta que contenga todos los formularios. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Si selecciona una carpeta la ejecución tardará 3 horas o más, depende del número de correcciones necesarias en los archivos. Es necesario conectarse a Internet.  Por favor no cerrar esta ventana mientras se está ejecutando. Usted puede controlar el avance de la ejecución en la consola.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Después de que hayan finalizado las correcciones y análisis de errores, en las siguientes pestañas, se encuentran tablas que muestran:</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Archivos con formato erróneo: Nombre de archivo y nombre de hoja que tienen un formato diferente. De las hojas Excel con formato erróneo, no se realizarán validaciones de ningún tipo.  </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Reporte de errores: Tabla que contiene nombre de archivo, nombre de hoja, nombre de atractor, lista de errores que presenta, zona, grupo y tramo.  </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Reporte de correcciones: Tabla que contiene los mismos encabezados de reporte de Errores. Pero que informa las correcciones que el programa ha realizado en los archivos. Para mayor información de las correcciones, se recomienda ver los manuales de usuario que han sido presentados.  </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Calles no reconocidas: Se encuentra una tabla que detalla nombre de archivo y nombre de la hoja que contiene calles que no se han podido reconocer ni encontrar una similitud aparente.</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Zona o grupo incorrectos: Se presenta una tabla que detalla nombre de archivo, nombre de hoja y tipo de error cuando la celda que almacena zona o grupo están vacías.</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Ver observaciones: En esta opción usted podrá seleccionar una carpeta que contenga formularios, de los cuales se mostrarán las Observaciones recolectadas.</li></ul>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Los errores y las correcciones se guardan a su vez en una base de datos de Validaciones contenida en el archivo denominado Vinculacion.accdb.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">La información correcta de las zonas y atractores no será agregada en la base de datos, mientras el programa siga reportando errores.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Cuando el programa no reporte ningún error, corrección o archivo con formato erróneo, la información habrá sido agregada exitosamente. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab), _translate("MainWindow", "Indicaciones"))
        self.label_11.setText(_translate("MainWindow", "ARCHIVOS CON FORMATO INCORRECTO"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_4), _translate("MainWindow", "Archivos con formato incorrecto"))
        self.label_4.setText(_translate("MainWindow", " REPORTES DE ERRORES"))
        self.label_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "TextLabel"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_2), _translate("MainWindow", "Reporte de errores"))
        self.label_10.setText(_translate("MainWindow", " REPORTE DE CORRECCIONES"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_3), _translate("MainWindow", "Reporte de correcciones"))
        self.label_19.setText(_translate("MainWindow", "CALLES NO RECONOCIDAS"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_6), _translate("MainWindow", "Calles no reconocidas"))
        self.label_23.setText(_translate("MainWindow", "ZONA O GRUPO VACÍOS"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_7), _translate("MainWindow", "Zona o grupo incorrectos"))
        self.btnVerObservaciones.setToolTip(_translate("MainWindow", "Al dar clic, podrá observar las observaciones que tienen los tramos de manera resumida en la tabla "))
        self.btnVerObservaciones.setText(_translate("MainWindow", "Ver observaciones"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_5), _translate("MainWindow", "Ver observaciones"))

class Ventana(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Validacion y verificacion de datos")
        self.setWindowIcon(QIcon("./imagenes/icono-ventana.png"))
        self.show()

"""if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())"""
