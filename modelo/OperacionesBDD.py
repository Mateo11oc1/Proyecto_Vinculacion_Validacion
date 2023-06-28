#Aqui para trabajar con lo de bdd
import pyodbc
import logging
class BaseDatos:
    def __init__(self):
        pass

    def crearConexionBDD(self, ruta_access):
        
        with pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+ruta_access) as self.connBDD:
            # Crea un cursor para ejecutar consultas
            self.cursorBDD = self.connBDD.cursor()
    
    def cerrarConexion(self):
        self.cursorBDD.close()
        self.connBDD.close()

    def almacenarErrores(self, ruta_access, columnasConErrores):
        self.crearConexionBDD(ruta_access)
        self.cursorBDD.execute("DELETE FROM detallescolumna")
        self.cursorBDD.execute("DELETE FROM error_detalle")
        
        for columna in columnasConErrores:
            iterador=0
            try:
                datosInsercion = (
                    columna["archivoNombre"], 
                    columna["nombreHoja"], 
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
                                columna["archivoNombre"], 
                                columna["nombreHoja"], 
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

        self.crearConexionBDD()
    
        try:
            self.cursorBDD.execute("SELECT id FROM correcciones WHERE descripcion = ?", nombreCorreccion)
            res = list(self.cursorBDD.fetchall())
            idCorrecion = res[0][0]
            print("Id correccion: " + str(idCorrecion))
        
            datosInsercion = (
                columna["archivoNombre"], 
                columna["nombreHoja"], 
                columna["atractor"], 
                columna["zona"], 
                columna["grupo"]
            )
            print(datosInsercion)
                        
            self.cursorBDD.execute("INSERT INTO DetalleCol_Correcciones (nombreArchivo, nombreHoja, atractor, zona, grupo) VALUES(?, ?, ?, ?, ?)", datosInsercion)
                        
            datosInsercion = (
                idCorrecion,
                columna["archivoNombre"], 
                columna["nombreHoja"], 
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
    