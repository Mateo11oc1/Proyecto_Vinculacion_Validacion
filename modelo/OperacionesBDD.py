#Aqui para trabajar con lo de bdd
import pyodbc
import logging
import time
import math
class BaseDatos:
    def __init__(self):
        self.ruta_access = "./Vinculacion.accdb"

    def crearConexionBDD(self, ruta_access):
        
        with pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+ruta_access) as self.connBDD:
            # Crea un cursor para ejecutar consultas
            self.cursorBDD = self.connBDD.cursor()
    
    def cerrarConexion(self):
        self.cursorBDD.close()
        self.connBDD.close()

    def almacenarErrores(self, columnasConErrores):
        self.crearConexionBDD(self.ruta_access)
        self.cursorBDD.execute("DELETE FROM detallescolumna")
        self.cursorBDD.execute("DELETE FROM error_detalle")
        
        for columna in columnasConErrores:
            iterador=0
            try:
                datosInsercion = (
                    columna["nombre_archivo"], 
                    columna["nombre_hoja"], 
                    columna["atractor"], 
                    columna["zona"], 
                    columna["grupo"]
                )
                print(datosInsercion)
                self.cursorBDD.execute("INSERT INTO detallescolumna (nombreArchivo, nombreHoja, atractor, zona, grupo) VALUES(?, ?, ?, ?, ?)", datosInsercion)
                
                for valor in columna["listaErrores"].values():
                    iterador+=1
                    if valor:
                            datosInsercion = (
                                iterador, 
                                columna["nombre_archivo"], 
                                columna["nombre_hoja"], 
                                columna["atractor"], 
                            )
                            print(datosInsercion)
                            self.cursorBDD.execute("INSERT INTO error_detalle (idError, nombreArchivo, nombreHoja, atractor) VALUES(?, ?, ?, ?)", datosInsercion)
                            
                            self.connBDD.commit()
                        
            except pyodbc.Error as e:
                logging.error("Error: %s", e)
                self.connBDD.rollback()
                                
        self.cerrarConexion()
                        
            
    def almacenarCorreccionesBDD(self, nombreCorreccion:str, columna):

        self.crearConexionBDD(self.ruta_access)
    
        try:
            self.cursorBDD.execute("SELECT id FROM correcciones WHERE descripcion = ?", nombreCorreccion)
            res = list(self.cursorBDD.fetchall())
            idCorrecion = res[0][0]
            print("Id correccion: " + str(idCorrecion))
        
            datosInsercion = (
                columna["nombre_archivo"], 
                columna["nombre_hoja"], 
                columna["atractor"], 
                columna["zona"], 
                columna["grupo"]
            )
            print(datosInsercion)
                        
            self.cursorBDD.execute("INSERT INTO DetalleCol_Correcciones (nombreArchivo, nombreHoja, atractor, zona, grupo) VALUES(?, ?, ?, ?, ?)", datosInsercion)
                        
            datosInsercion = (
                idCorrecion,
                columna["nombre_archivo"], 
                columna["nombre_hoja"], 
                columna["atractor"], 
            )
                        
            self.cursorBDD.execute("INSERT INTO correccion_detalle (idCorreccion, nombreArchivo, nombreHoja, atractor) VALUES(?, ?, ?, ?)", datosInsercion)
                        
            self.connBDD.commit()
        except pyodbc.Error as e:
            print(datosInsercion)
            # time.sleep(10)
            logging.error("Error al ejecutar la consulta: %s", e)
            self.connBDD.rollback()
        self.cerrarConexion()
    
    
    def almacenarTramo(self, columna: dict):
        
        try:
            
            datosInsercion = (
                columna["hoja"],
                columna["zona"], 
                1, 
                columna["tramo"], 
            )
            print("Almacenar tramo:" + str(datosInsercion))
                        
            self.cursorBDD.execute("INSERT INTO Tramo (numTramo, idZona, id_calle_principal, nombre) VALUES(?, ?, ?, ?)", datosInsercion)
            return True
        except pyodbc.Error as e:
            print(datosInsercion)
            # time.sleep(10)
            logging.error("Error al ejecutar la consulta: %s", e)
            return False
        
    def almacenar_horario_jornada_tam(self, columna: dict):
        datosInsercion = []
        
        def almacenarHorario(listaHorario: list):
            for hor in listaHorario:
                if math.isnan(hor):
                    datosInsercion.append(0)
                else:
                    datosInsercion.append(hor)
            
            print("Almacenar horario: " + str(datosInsercion))
            self.cursorBDD.execute("INSERT INTO horario (num_lunes, num_martes, num_miercoles, num_jueves, num_viernes, num_sabado, " + 
                                    "num_domingo, num_todos_dias, num_entre_semana, num_fin_semana) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                                    datosInsercion)
        
        def almacenarJornada(listaJornada: list):
            datosInsercion = []
            for jor in listaJornada:
                if math.isnan(jor):
                    datosInsercion.append(0)
                else:
                    datosInsercion.append(jor)
            
            print("AlmacenarJornada: " + str(datosInsercion))
            self.cursorBDD.execute("INSERT INTO jornada (num_matutino, num_vespertino, num_diurno, num_nocturno, num_todo_dia) " + 
                                    "VALUES (?, ?, ?, ?, ?)", datosInsercion)
        
        def almacenarTamanio(listaTam: list):
            datosInsercion = []
            for tam in listaTam:
                if math.isnan(tam):
                    datosInsercion.append(0)
                else:
                    datosInsercion.append(tam)
            
            print("Almacenar tamanio: " + str(datosInsercion))
            self.cursorBDD.execute("INSERT INTO tamanio (num_pequenios, num_medianos, num_grandes) VALUES (?, ?, ?)", datosInsercion)
        
        try:
            almacenarTamanio(columna["tamanio"])
            almacenarJornada(columna["jornada"])
            almacenarHorario(columna["dias"])
            return True
        except pyodbc.Error as e:
            print(datosInsercion)
            # time.sleep(10)
            logging.error("Error al ejecutar la consulta: %s", e)
            return False
        
    def almacenarCaracteristica(self, caracteristica:tuple, columna:dict, idAtractor):
        
        try:
            
            datosInsercion = (columna["zona"], columna["hoja"], idAtractor) + caracteristica
            print("Almacenar caracteristica: " + str(datosInsercion))
                        
            self.cursorBDD.execute("INSERT INTO Tramo_atractor_caracteristica (idZona, idTramo, idAtractor, idHorario, idJornada, idTamanio) "+
                                "VALUES (?, ?, ?, ?, ?, ?)", datosInsercion)
            return True
        except pyodbc.Error as e:
            print(datosInsercion)
            # time.sleep(10)
            logging.error("Error al ejecutar la consulta: %s", e)
            return False
        
    def separarTamanio(self, listaTamanios: list):
        tamanioLetras = {}
        contador = 0
        tamanios = {0: "G", 1: "M", 2: "P"}
    
        for tam in listaTamanios:

            if not math.isnan(tam):
                tamanioLetras[tamanios[contador]] = tam
            else:
                tamanioLetras[tamanios[contador]] = 0
            contador += 1
        return tamanioLetras
    
    def insertarTablaOferta(self, listaTamanios: dict, columna: dict, idAtractor):
        
        for tam, num in listaTamanios.items():
            try:
                if num > 0:
                    datosInsercion = (columna["zona"], columna["hoja"], idAtractor, tam, num)
                    print("Almacenar oferta: " + str(datosInsercion))
                    self.cursorBDD.execute("INSERT INTO oferta (idZona, idTramo, idTipoAtractor, tamanio, cantidadAtractores) VALUES (?, ?, ?, ?, ?)", datosInsercion)
                    
            except pyodbc.Error as e:
                print(datosInsercion)
                # time.sleep(10)
                logging.error("Error al ejecutar la consulta: %s", e)
                
    
    def insercionBDD(self, columnas_sin_errores: list):
        
        def consultarAtractor(atractor: str):
            print(atractor)
            self.cursorBDD.execute("SELECT * FROM TipoAtractor WHERE nombre LIKE ?", ('%' + atractor + '%',))
            
            resultado = self.cursorBDD.fetchone()
            print(resultado)
            if resultado:
                return resultado[0]
            else: 
                return None
        
        def consultarCaracteristica():
            
            self.cursorBDD.execute("SELECT TOP 1 id FROM horario ORDER BY id DESC;")
            resultado = self.cursorBDD.fetchone()
            
            retorno = [resultado[0]]
            
            self.cursorBDD.execute("SELECT TOP 1 id FROM jornada ORDER BY id DESC;")
            resultado = self.cursorBDD.fetchone()
            retorno.append(resultado[0])
            
            self.cursorBDD.execute("SELECT TOP 1 id FROM tamanio ORDER BY id DESC;")
            resultado = self.cursorBDD.fetchone()
            retorno.append(resultado[0])

            return retorno
        
        self.crearConexionBDD(self.ruta_access)
        for col in columnas_sin_errores:
            try:
                print(str(col) + "\n") 
                self.almacenarTramo(col)
                # time.sleep(30)
                self.almacenar_horario_jornada_tam(col)
                # time.sleep(30)
                self.almacenarCaracteristica(tuple(consultarCaracteristica()), col, consultarAtractor(col["atractor"]))
                # time.sleep(30)
                self.insertarTablaOferta(self.separarTamanio(col["tamanio"]), col, consultarAtractor(col["atractor"]))
                self.connBDD.commit()
            except pyodbc.Error as e:
                print("Se hara rollback debido a un error")
                print(e)
                self.connBDD.rollback()
        