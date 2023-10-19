#Aqui para trabajar con lo de bdd
import pyodbc
import logging
import time
import math
from unidecode import unidecode
class BaseDatos:
    def __init__(self):
        self.ruta_access = "source/Vinculacion.accdb"

    def crearConexionBDD(self, ruta_access):
        
        with pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+ruta_access) as self.connBDD:
            # Crea un cursor para ejecutar consultas
            self.cursorBDD = self.connBDD.cursor()
    
    def cerrarConexion(self):
        self.cursorBDD.close()
        self.connBDD.close()

    
    def almacenarTramo(self, calles: dict):
        
        try:
            
            datosInsercion = (
                calles["tramo"],
                calles["zona"], 
                calles["principal"][0], 
                calles["nombreTramo"], 
            )
            print("Almacenar tramo:" + str(datosInsercion))
                        
            self.cursorBDD.execute("INSERT INTO Tramo (numTramo, idZona, idCallePrincipal, nombre) VALUES(?, ?, ?, ?)", datosInsercion)
            for calle in calles["secundarias"]:
                print(calle)
                query = f'INSERT INTO calle_secundaria_tramo (idTramo, idZona, idCalle) VALUES({calles["tramo"]}, {calles["zona"]}, {calle[0]})'
                print(query)
                self.cursorBDD.execute(query)
                
            return True
        except pyodbc.IntegrityError as e:
            logging.error("La correccion ya ha sido agregada a la Base de Datos: %s", e)
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
        except pyodbc.IntegrityError as e:
            logging.error("Característica ya almacenada anteriormente en la base de datos: %s", e)
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
        except pyodbc.IntegrityError as e:
            logging.error("Característica ya almacenada anteriormente en la base de datos: %s", e)
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
                    datosInsercion = (columna["zona"], columna["hoja"], idAtractor,1, tam, num)
                    print("Almacenar oferta: " + str(datosInsercion))
                    self.cursorBDD.execute("INSERT INTO oferta (idZona, idTramo, idTipoAtractor, idMotivoAtraccion, tamanio, cantidadAtractores) VALUES (?, ?, ?, ?, ?, ?)", datosInsercion)
            except pyodbc.IntegrityError as e:
                logging.error("Característica ya almacenada anteriormente en la base de datos: %s", e)
            except pyodbc.Error as e:
                print(datosInsercion)
                # time.sleep(10)
                logging.error("Error al ejecutar la consulta: %s", e)
                
    def buscarCalleBDD(self, calle: str):
        self.crearConexionBDD(self.ruta_access)
        print("Calle archivo: ", unidecode(str.upper(calle)))
        # time.sleep(2)
        self.cursorBDD.execute("SELECT * FROM calle WHERE nombre LIKE ?", unidecode(str.upper(calle)))
        resultado = self.cursorBDD.fetchone()
        print("\nResultado busqueda: " + str(resultado))
        self.cerrarConexion()
        return resultado
    
    def ingresarCalle(self, calle: str):
        try:
            self.crearConexionBDD(self.ruta_access)
            self.cursorBDD.execute("INSERT INTO calle (nombre) VALUES (?)", calle)
            self.connBDD.commit()
            self.cerrarConexion()
        except pyodbc.IntegrityError as e:
            logging.error("Calle ya almacenada anteriormente en la base de datos: %s", e)
        except pyodbc.Error as e:
            print("Error al ingrear la calle\n")
            print(e)
            self.connBDD.rollback()
            self.cerrarConexion()
            
    def insercionBDD(self, calles_tramos:dict, columnas_sin_errores: list):
        
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
        for i in columnas_sin_errores:
            print(i)
            print("\n")
        self.crearConexionBDD(self.ruta_access)
        for calle in calles_tramos:
            hoja = columnas_sin_errores[0]["hoja"]
            try:
                self.almacenarTramo(calle)
                borrar = []
                for col in columnas_sin_errores:
                    if col["hoja"] == hoja:
                        print(str(col) + "\n") 
                        
                        # time.sleep(10)
                        self.almacenar_horario_jornada_tam(col)
                        # time.sleep(10)
                        self.almacenarCaracteristica(tuple(consultarCaracteristica()), col, consultarAtractor(col["atractor"]))
                        # time.sleep(10)
                        self.insertarTablaOferta(self.separarTamanio(col["tamanio"]), col, consultarAtractor(col["atractor"]))
                        self.connBDD.commit()
                        borrar.append(col)
                        
                    else:
                        hoja = col["hoja"]
                        columnas_sin_errores = [i for i in columnas_sin_errores if i not in borrar]
                        break
            except pyodbc.IntegrityError as e:
                logging.error("Tramo ya almacenado anteriormente en la base de datos: %s", e)
            except pyodbc.Error as e:
                print("Se hara rollback debido a un error en ingresar tramo")
                print(e)
                self.connBDD.rollback()
            
        self.cerrarConexion()

##############################################################################################################################
#Ingreso de errores y correcciones en la BDD
    def almacenarTodosLosErrores(self, columnasConErrores, hojasMalFormato, hojasZonaGrupoMal, callesNoReconocidas): #este metodo llama a todas las funciones de abajo exceptuando almacenarCorrecciones
        self.almacenarErrores(columnasConErrores)
        self.almacenarFormatoIncorrecto(hojasMalFormato)
        self.almacenarZonaOGrupoIncorrectos(hojasZonaGrupoMal)
        self.almacenarCallesNoReconocidas(callesNoReconocidas)


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
            except pyodbc.IntegrityError as e:
                logging.error("Error ya almacenado anteriormente en la base de datos: %s", e)            
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
        except pyodbc.IntegrityError as e:
            logging.error("Correccion ya almacenada anteriormente en la base de datos: %s", e)
        except pyodbc.Error as e:
            print(datosInsercion)
            # time.sleep(10)
            logging.error("Error al ejecutar la consulta: %s", e)
            self.connBDD.rollback()
        self.cerrarConexion()

    def almacenarFormatoIncorrecto(self, hojasConFormatoIncorrecto):
        self.crearConexionBDD(self.ruta_access)
        self.cursorBDD.execute("DELETE FROM FormatoIncorrecto")
        iterador=1
        for hoja in hojasConFormatoIncorrecto:
            
            try:
                datosInsercion = (
                    iterador,
                    hoja["nombre_archivo"], 
                    hoja["nombre_hoja"]
                )
                print(datosInsercion)
                self.cursorBDD.execute("INSERT INTO FormatoIncorrecto (id, nombreArchivo, nombreHoja) VALUES(?, ?, ?)", datosInsercion)
                self.connBDD.commit()
                iterador+=1      
            except pyodbc.IntegrityError as e:
                logging.error("Hoja con formato incorrecto ya almacenada anteriormente en la base de datos: %s", e)  
            except pyodbc.Error as e:
                logging.error("Error: %s", e)
                self.connBDD.rollback()
                                
        self.cerrarConexion()

    def almacenarZonaOGrupoIncorrectos(self, hojasConZonaOGrupoIncorrecto):
        self.crearConexionBDD(self.ruta_access)
        self.cursorBDD.execute("DELETE FROM ZonaOGrupoIncorrectos")
        iterador=1
        for hoja in hojasConZonaOGrupoIncorrecto:
            
            try:
                datosInsercion = (
                    iterador,
                    hoja["nombre_archivo"], 
                    hoja["nombre_hoja"], 
                    hoja["zona"],
                    hoja["grupo"], 
                    hoja["errores"]
                )
                print(datosInsercion)
                self.cursorBDD.execute("INSERT INTO ZonaOGrupoIncorrectos (id, nombreArchivo, nombreHoja, zona, grupo, errores) VALUES(?, ?, ?, ?, ?, ?)", datosInsercion)
                self.connBDD.commit()
                iterador+=1
            except pyodbc.IntegrityError as e:
                logging.error("Error ya almacenado anteriormente en la base de datos: %s", e)
            except pyodbc.Error as e:
                logging.error("Error: %s", e)
                self.connBDD.rollback()
                                
        self.cerrarConexion()
    
    def almacenarCallesNoReconocidas(self, listaCalles):
        self.crearConexionBDD(self.ruta_access)
        self.cursorBDD.execute("DELETE FROM callesNoReconocidas")
        iterador=1
        for calle in listaCalles:
            
            try:
                datosInsercion = (
                    iterador,
                    calle["nombre_archivo"], 
                    calle["nombre_hoja"], 
                    calle["calle"],
                    calle["tipo"]                
                )
                print(datosInsercion)
                self.cursorBDD.execute("INSERT INTO callesNoReconocidas (id, nombreArchivo, nombreHoja, calle, tipoCalle) VALUES(?, ?, ?, ?, ?)", datosInsercion)
                self.connBDD.commit()
                iterador+=1
            except pyodbc.IntegrityError as e:
                logging.error("Calle no reconocida ya almacenada anteriormente en la base de datos: %s", e)
            except pyodbc.Error as e:
                logging.error("Error: %s", e)
                self.connBDD.rollback()
                                
        self.cerrarConexion()