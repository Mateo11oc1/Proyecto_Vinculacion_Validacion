import os
import glob
import pandas
import math
import traceback
import time
import xlwings 
import re
import tkinter as tk
from tkinter import messagebox
from modelo.OperacionesBDD import BaseDatos
from modelo.generarLogs import GenerarLogs
from modelo.manejoCalles import ManejoCalles
#Las validaciones devuelve un valor de true si es que la columna presenta el error especificado, caso contrario, devuelve false
#El detalle de los errores se encuentra en la clase GenerarLogs y se llama self.diccionarioErrores:

class Validaciones:

    def __init__(self):
        self.ruta_access=r"./Vinculacion.accdb"  #cambiar segun el nombre del archivo, la ruta es relativa
        self.baseDatos = BaseDatos()
        self.generarLogs=GenerarLogs()
        self.manejoCalles=ManejoCalles()
        self.archivos_excel = []
        self.columnasSinErrores = []
        self.contadorCorrecciones=0

    def leerCarpeta(self, carpeta):
        # Obtener todos los archivos en la carpeta que tengan la extensión .xlsx
        self.archivos_excel = [archivo for archivo in  glob.glob(os.path.join(carpeta, '*.xlsx')) if not os.path.basename(archivo).startswith("~$")]
        
    #este metodo valida que las hojas tengan formato correcto retornando True si hay un error de formato
    #un error de formato es si la tabla esta movida hacia arriba, abajo, derecha o izquierda
    def validarFormatoIncorrecto(self, nombre_hoja, nombre_archivo, hoja_leida):
        
        
        try:

            if hoja_leida.iloc[1,1]=="Grupo:" and hoja_leida.iloc[2,1]=="Zona:" and hoja_leida.iloc[6,2]=="Educación" and hoja_leida.iloc[9,1]=="# Atractores" and hoja_leida.iloc[7, 2]=="Escuela/Colegio" and hoja_leida.iloc[7,54]=="Edificio de Departamentos":               
                pass
            else:
                print("Error de formato en la hoja "+nombre_hoja+" del archivo "+os.path.basename(nombre_archivo)+"\n")
                return True
        except IndexError as e:
            print("Error de formato en la hoja "+nombre_hoja+" del archivo "+os.path.basename(nombre_archivo)+"\n")
            #print(str(e))
            return True  #si se produce una excepcion es porque no se pudo acceder a una de las celdas, se retorna True porque significa que la celda esta vacia y tiene mal formato

    
    #opcion es para ver si se ha seleccionado un solo archivo(1) o una carpeta(2), este metodo es llamado desde el controlador
    def procesar_archivos_excel(self, opcion, validarCalles:bool):
        self.listaFormatoIncorrecto=[]
        self.listaColumnas = []
        self.columnasConErrores = []
        self.columnasConCorrecciones=[]
        self.listaZonaOGrupoNan=[]
        #Recorro todos los archivos, i-> nombreArchivo
        print(self.archivos_excel)
        for i in self.archivos_excel:
            
            try:
            #Leo todas las hojas de una vez del documento
                leido = pandas.read_excel(i, sheet_name = None)
                numHoja = 1
                #Recorro cada hoja del archivo
                for nombreHoja, hoja in leido.items():
                    
                    if not self.validarFormatoIncorrecto(nombreHoja, i, hoja): #si el formato de la hoja no es incorrecto
                        self.validarZonaOGrupoNan(hoja, i, nombreHoja)
                        #Recorro cada columna
                        for columna in range(2, 55):
                            #Desde la fila 7 en adelante porque alli empiezan los datos que interesan almacenar(nombre de atractor, numero,dias,jornada, tamanio)
                            lista = hoja.iloc[7:, columna].values.tolist()
                            columna = { "atractor": lista[0], "numAtractores":lista[2], "tamanio": lista[3:6], "jornada": lista[6:11],
                                    "dias": lista[12:22], "numColumna": columna, "hoja": numHoja, "archivoRuta": i, "nombre_archivo": os.path.basename(i), 
                                    "vacia":False, "listaErrores":{1:False, 2:False,3:False,4:False,5:False, 6:False,7:False,8:False, 9:False}, "grupo": hoja.iloc[1, 2], "zona":hoja.iloc[2, 2], "tramo": hoja.iloc[1, 12],
                                    "observaciones":hoja.iloc[30,1], "nombre_hoja": nombreHoja, "listaCorrecciones":{1:False, 2:False,3:False,4:False} }
                            #os.path.basename(i) es para q solo se escriba el nombre del archivo, no toda la ruta
                            #inicializamos los valores de listaErrores y listaCorrecciones en False porque cambia a True si hay un error o se ha realizado una correccion
                            columna = self.validar(columna)
                            
                            if columna != None: #si la columna no esta vacia
                                print(f'---------\nArchivo: {columna["nombre_archivo"]}\n Nombre Hoja: {columna["nombre_hoja"]}\nNum Hoja: {columna["hoja"]}\n Columna: {columna["numColumna"]}\nAtractor: {columna["atractor"]}')
                                self.listaColumnas.append(columna)
                                valida = 0
                                for error in columna["listaErrores"].values():
                                    if error: #si encuentra un True significa que hay al menos un error
                                        valida = 1
                                        self.columnasConErrores.append(columna)
                                        break
                                    
                                if columna not in self.columnasSinErrores and valida == 0:
                                    self.columnasSinErrores.append(columna)
                                    columnaInsercion = columna
                                    
                                for correccion in columna["listaCorrecciones"].values():
                                    if correccion:
                                        self.columnasConCorrecciones.append(columna)
                                        break
                        if validarCalles==True:
                            try:
                                calles = self.manejoCalles.compararCalles(self.manejoCalles.almacenarCalles_Tramo(hoja, os.path.basename(i), nombreHoja))      
                            except Exception as e:
                                print(str(e))
                            self.manejoCalles.calles_tramos.append({**{"zona":columnaInsercion["zona"], "tramo":columnaInsercion["hoja"], "nombreTramo":columnaInsercion["tramo"]}, **calles})
                    else:
                        malformato={"nombre_archivo":os.path.basename(i),"nombre_hoja": nombreHoja }
                        self.listaFormatoIncorrecto.append(malformato)
                    numHoja += 1    
            except Exception as e:
                print(f"Ocurrio una excepcion:", str(e))
                traceback.print_exc()
                
        
        
        self.ingresoBDD(opcion, validarCalles)
        self.manejoCalles.reintentarConectarCalles()
        self.baseDatos.almacenarTodosLosErrores(self.columnasConErrores, self.listaFormatoIncorrecto, self.listaZonaOGrupoNan, self.manejoCalles.hojasConCallesInvalidas)
        self.generarLogs.generarArchivosLog(self.columnasConErrores, self.listaFormatoIncorrecto, self.manejoCalles.hojasConCallesInvalidas, self.listaZonaOGrupoNan)   #genera archivos logs que contienen la misma informacion de la interfaz

        return self.columnasConErrores, self.columnasConCorrecciones, self.listaFormatoIncorrecto, self.manejoCalles.hojasConCallesInvalidas, self.listaZonaOGrupoNan


    #metodo con el cual se llama a ingresar toda la informacion de zona, tramo, calles, atractores, tamanio, jornada
    def ingresoBDD(self, opcion, se_validaron_Calles):
        if se_validaron_Calles:
            if len(self.columnasConErrores) == 0 and len(self.manejoCalles.hojasConCallesInvalidas) == 0 and len(self.listaFormatoIncorrecto) == 0 and opcion == 1:
            
                self.baseDatos.insercionBDD(self.manejoCalles.calles_tramos, self.columnasSinErrores)
        
    

    def verObservacionesArchivos(self)->list:
        self.listaColumnas = []
        self.archivoConObservaciones = []
        #Recorro todos los archivos
        for i in self.archivos_excel:
            #Leo todas las hojas de una vez del documento
            try:
                leido = pandas.read_excel(i, sheet_name = None)
            except Exception as e:
                print(f"Error en el archivo {i}")
            numHoja = 0
            #Recorro cada hoja
            for nombreHoja, j in leido.items():
                #Recorro cada columna
                #shape[1] nos da el numero de columnas de la hoja
                if not self.validarFormatoIncorrecto(nombreHoja, i,j):
                    try:
                        archivo={"hoja":numHoja, "nombre_archivo":os.path.basename(i), "grupo": j.iloc[1, 2], "zona":j.iloc[2, 2], "tramo": j.iloc[1, 12],
                            "observaciones":j.iloc[30,1], "nombre_hoja":nombreHoja}
                        print(f'---------\nArchivo: {archivo["nombre_archivo"]}\n Hoja: {archivo["nombre_hoja"]}')
                        #Si las observaciones no estan vacias
                        if archivo["observaciones"] is not None and not pandas.isna(archivo["observaciones"]):
                            self.archivoConObservaciones.append(archivo)

                        numHoja += 1
                    except Exception as e:
                        print(f"Error en el archivo {i}. \nHoja: {nombreHoja} {e}")
    
        return self.archivoConObservaciones


    #Si una columna esta vacia no sera necesario realizar las validaciones
    def validarColVacia(self, columna: dict) -> list:
        def listaVacia(lista):
            for i in lista:
                if not math.isnan(i):
                    return False
            return True
        #Si hay un TypeError automaticamente no esta vacia
        try:
            #Si todo es NaN, la columna esta vacia
            if math.isnan(columna["numAtractores"]) and listaVacia(columna["tamanio"]) and listaVacia(columna["jornada"]) and listaVacia(columna["dias"]):
                columna["vacia"] = True
                return [columna, True]
            else:
                columna["vacia"] = False
                return [columna, False]
        except TypeError:
            columna["vacia"] = False
            return [columna, False]

    #Validar que solo sean numeros y no letras
    def validarCaracteres(self, columna: dict) -> list:
        #si no es un numero entero
        #si en numero de atractores hay un dato tipo string
        if isinstance(columna["numAtractores"], str):
            #logging.error("Numero de atractores no es un entero")
            columna["listaErrores"][1] = True
            return [columna, True]
        #si en numero de atractores hay un flotante
        if isinstance(columna["numAtractores"], float):
            #se condiciona que no sea NaN porque puede haber una celda vacia en numero de atractores que contenga
            #datos en el resto de la columna y que tenga que ser validado despues, entonces no debe entrar al if
            if isinstance(columna["numAtractores"], float) and not math.isnan(columna["numAtractores"]):
                #Esto reporta en consola como si fuera un error
                #logging.error("Numero de atractores no es un entero")
                columna["listaErrores"][1] = True
                return [columna, True]


        #se recorre la lista de valores de la columna desde 2 en adelante porque va desde el tamanio
        for i in list(columna.values())[2:5]:
            #se recorre cada lista, porque hay la lista tamanio, jornada, dias
            for j in i:
                #si el valor de la celda es un string, esta vacio o es un numero decimal
                if isinstance(j, str) or (not math.isnan(j) and not isinstance(j, int)):
                    #logging.error("El valor no es un numero")
                    columna["listaErrores"][1] = True
                    return [columna, True]

        #El indice [1], hace referencia a la clave del error de que un valor de la columna es decimal o un caracter
        columna["listaErrores"][1] = False
        return [columna, False]

    #Valida que los datos de tamanio, no estan vacios
    def validarTamanioDatosVacios(self, columna: dict) -> list:

        for i in columna["tamanio"]:
            bandera = 0
            #Si un elemento de los tamanios no esta vacio, no tiene este error
            if not math.isnan(i):
                bandera = 1
                columna["listaErrores"][2] = False
                return [columna, False]

        #Si la bandera no cambia, significa que los datos de tamanio estan vacios
        if bandera == 0:

            columna["listaErrores"][2] = True
            return [columna, True]

    #Valida que la suma de los tamanios sea igual al numero de atractores colocados
    def validarSumaTamanio(self, columna: dict) -> list:

        #si es que hay algo en la celda se valida que el numero de atractores sea igual a la suma de los tamanos
        if columna["numAtractores"] == sum(x for x in columna["tamanio"] if not math.isnan(x)):
            columna["listaErrores"][3] = False
            return [columna, False] #no hay el error
        else:
            columna["listaErrores"][3] = True
            return [columna, True] #si hay el error

    #Modifica en el archivo el numero de atractores en caso de que sea vacio y que se pueda sumar desde la columna de tamanios
    def modificarCampoNAtractores(self, columna: dict) -> list:
        #si el numero de atractores es nulo

        if math.isnan(columna["numAtractores"]):
            # abre la aplicación de Excel en segundo plano
            app = xlwings.App(visible=False)   
            try:
                
            # abrir el archivo
                wb = xlwings.Book(columna["archivoRuta"])
                
                
            except Exception as e:
                print("No se pudo realizar la correccion porque el archivo esta danado")
                return
            # seleccionar la hoja
            hoja = wb.sheets[columna["nombre_hoja"]]
                # modificar el valor de una celda
            hoja.cells(11, columna["numColumna"]+1).value = sum(x for x in columna['tamanio'] if not math.isnan(x))
            # guarda los cambios y cierra excel
            wb.save()
            wb.close()
            app.quit()
            print("Corrigiendo numero de atractores...")
            self.contadorCorrecciones+=1
            self.generarLogs.generarArchivoCorreccionesRealizadas("Se ha escrito el total(sumando los tamanios) de atractores en # Atractores porque era un campo vacío", columna, self.contadorCorrecciones)
            self.baseDatos.almacenarCorreccionesBDD("Se ha escrito el número de atractores en #Atractores", columna)
            columna["listaCorrecciones"][1] = True
            columna["listaErrores"][2] = False #como ya se ha realizado la correccion ya no se presenta el error 2 ni 3 
            columna["listaErrores"][3]=False


    #Valida que los datos de jornada, no estan vacios
    def validarJornadaDatosVacios(self, columna: dict) -> list:

        for i in columna["jornada"]:
            bandera = 0
            #Si un elemento de los jornada no esta vacio, no tiene este error
            if not math.isnan(i):
                bandera = 1
                columna["listaErrores"][4] = False
                return [columna, False]

        #Si la bandera no cambia, significa que los datos de jornada estan vacios
        if bandera == 0:
            columna["listaErrores"][4] = True
            return [columna, True]


    #Validar que la suma de todos los datos en jornada no sea menor al numero de atractores
    #Por ejemplo hay 3 atractores tipo Restaurante, se indica que hay 1 matutino y 1 nocturno, la suma de ambos es 2<al numero de atractores
    def validarSumaJornada(self, columna:dict) -> list:

        #si el numero de atractores es mayor a la suma de los valores del jornada
        if columna["numAtractores"] > sum(x for x in columna['jornada'] if not math.isnan(x)):
            columna["listaErrores"][5] = True
            return [columna, True] #si hay el error
        else:
            columna["listaErrores"][5] = False
            return [columna, False] #no hay el error


    #Validar que uno o varios de los datos de la jornada no sobrepase el numero de atractores
    #No se valida que esto se cumpla con la suma de los datos de la jornada debido a que se puede tener un atractor que sea matutino y nocturno a la vez
    #Por ejemplo hay 3 atractores tipo Restaurante se indica que hay 4 diurnos lo cual es incorrecto
    def validarJornadaNoSobrepaseAtractores(self, columna:dict) -> list:
        for i in columna['jornada']:
            if columna["numAtractores"] < i:
                columna["listaErrores"][6] = True
                return [columna, True]

        columna["listaErrores"][6] = False
        return [columna, False]


    #En caso de que este marcado matutino y vespertino y sea igual al numero de atractores total, se marca en el archivo como diurno
    #Se borra en matutimo y vespertino
    #ejemplo:hay 3 atractores que atienen horario matutino y vespertino, se sustituye con 3 atractores que atienden en horario diurno
    def corregirDiurno(self, columna: dict) -> list:

        if not math.isnan(sum(x for x in columna["jornada"] if not math.isnan(x))):
                
            if not math.isnan(columna["jornada"][0]) and not math.isnan(columna["jornada"][1]) and columna["jornada"][0] == columna["numAtractores"] and columna["jornada"][1] == columna["numAtractores"]:
                

                # abre la aplicación de Excel en segundo plano
                app = xlwings.App(visible=False)

                # abrir el archivo
                try:
                    wb = xlwings.Book(columna["archivoRuta"])
                    
                except Exception as e:
                    print("\nNo se puede realizar la correccion de diurno porque el archivo esta dañado")
                    return
                # seleccionar la hoja
                hoja = wb.sheets[columna["nombre_hoja"]]

                # modificar el valor de una celda
                hoja.cells(17, columna["numColumna"]+1).value = sum(x for x in columna['tamanio'] if not math.isnan(x))
                hoja.cells(15, columna["numColumna"]+1).value = ""
                hoja.cells(16, columna["numColumna"]+1).value = ""

                # guarda los cambios y cierra excel
                wb.save()
                wb.close()
                app.quit()
                print("Corrigiendo diurno...")
                self.contadorCorrecciones+=1
                self.generarLogs.generarArchivoCorreccionesRealizadas("Se ha cambiado los datos de #vespertino y #matutino por #diurno", columna, self.contadorCorrecciones)
                self.baseDatos.almacenarCorreccionesBDD("Se ha cambiado los datos de #vespertino y #matutino por #diurno", columna)
                columna["listaCorrecciones"][2] = True               
            
    #Valida que los datos de dias, no estan vacios
    def validarDiasDatosVacios(self, columna: dict) -> list:

        for i in columna["dias"]:
            bandera = 0
            #Si un elemento de los dias no esta vacio, no tiene este error
            if not math.isnan(i):
                bandera = 1
                columna["listaErrores"][7] = False
                return [columna, False]

        #Si la bandera no cambia, significa que los datos de dias estan vacios
        if bandera == 0:
            columna["listaErrores"][7] = True
            return [columna, True]

    #Validar que uno o varios de los datos de los días de atención no sobrepasen el numero de atractores
    #No se valida que esto se cumpla con la suma de los datos de los días de atención debido a que se puede tener un atractor
    #que atienda lunes y martes a la vez
    def validarDiasNoSobrepaseAtractores(self, columna:dict) -> list:
        for i in columna['dias']:
            if columna["numAtractores"] < i:
                columna["listaErrores"][8] = True
                return [columna, True]

        columna["listaErrores"][8] = False
        return [columna, False]


    #Validar que la suma de todos los datos en dias no sea menor al numero de atractores
    def validarSumaDias(self, columna:dict) -> list:

        #si el numero de atractores es mayor a la suma de los valores del dias
        if columna["numAtractores"] > sum(x for x in columna["dias"] if not math.isnan(x)):
            columna["listaErrores"][9] = True
            return [columna, True] #si hay el error
        else:
            columna["listaErrores"][9] = False
            return [columna, False] #no hay el error


    #esta funcion sirve para el caso de que hayan atractores que tengan marcado lunes, martes, miercoles, jueves y viernes en vez de
    #entre semana
    def corregirEntreSemana(self, columna: dict) -> list:

        if not math.isnan(sum(x for x in columna["dias"] if not math.isnan(x))):
            #si la lista de dias de las posiciones 1 al 5 que contiene los datos de lunes, martes, miercoles jueves y viernes
            #es igual al numero de atractores
            if all(dia == columna["numAtractores"]  for dia in columna["dias"][:5]) and all(math.isnan(dia) for dia in columna["dias"][5:]):
                
                            
                # abre la aplicación de Excel en segundo plano
                app = xlwings.App(visible=False)
                try:
                # abrir el archivo
                    wb = xlwings.Book(columna["archivoRuta"])
                except Exception as e:
                    print("\nNo se puede realizar la correccion de entre semana porque el archivo esta dañado")
                    return
                # seleccionar la hoja
                hoja = wb.sheets[columna["nombre_hoja"]]

                # modificar el valor la celda entre semana 
                hoja.cells(30, columna["numColumna"]+1).value = columna["numAtractores"]
                hoja.cells(25, columna["numColumna"]+1).value = ""
                hoja.cells(24, columna["numColumna"]+1).value = ""
                hoja.cells(23, columna["numColumna"]+1).value = ""
                hoja.cells(22, columna["numColumna"]+1).value = ""
                hoja.cells(21, columna["numColumna"]+1).value = ""

                # guarda los cambios y cierra excel
                wb.save()
                wb.close()
                app.quit()
                print("Corrigiendo entre semana...")
                self.contadorCorrecciones+=1
                self.generarLogs.generarArchivoCorreccionesRealizadas("Se ha cambiado #lunes, #martes, #miercoles, #jueves, #viernes por #entre semana", columna, self.contadorCorrecciones)
                self.baseDatos.almacenarCorreccionesBDD("Se ha cambiado #lunes, #martes, #miercoles, #jueves, #viernes por #entre semana", columna)
                columna["listaCorrecciones"][3] = True

    # Verifica y modifica si hay datos escritos en filas de abajo en las columnas de vivienda
    def validarViviendas(self, columna: dict):
        def validar(columna: dict):
            if columna["atractor"] == "Casa/Villa" or columna["atractor"] == "Edificio de Departamentos":
                listaUnida = list(columna.values())[2] + list(columna.values())[3] + list(columna.values())[4] 
                for i in listaUnida:
                    if not math.isnan(i) and math.isnan(columna["numAtractores"]):
                        return False, i, listaUnida.index(i)
            return True, 0, 0
        
        validado = validar(columna)
        if not validado[0]:
            
                            
            # abre la aplicación de Excel en segundo plano
            app = xlwings.App(visible=False)
            try:
            # abrir el archivo
                wb = xlwings.Book(columna["archivoRuta"])

                
            except Exception as e:
                print("No se pudo corregir la vivienda porque el archivo esta dando")
                return

            # seleccionar la hoja
            hoja = wb.sheets[columna["nombre_hoja"]]

            columna["numAtractores"] = validado[1]
            # modificar el valor la celda entre semana 
            hoja.cells(11, columna["numColumna"]+1).value = validado[1]
            hoja.cells(11 + validado[2] + 1, columna["numColumna"]+1).value = ""

            # guarda los cambios y cierra excel
            wb.save()
            wb.close()
            app.quit()
            print("Corrigiendo viviendas...")
            self.contadorCorrecciones+=1
            self.generarLogs.generarArchivoCorreccionesRealizadas("Se ha modificado el número de atractores en el motivo Vivienda ya que se encontraba en filas inferiores", columna, self.contadorCorrecciones)
            self.baseDatos.almacenarCorreccionesBDD("Se ha modificado el número de atractores en el motivo Vivienda ya que se encontraba en filas inferiores", 
                                                    columna)
            columna["listaCorrecciones"][4] = True

    #la celda que contiene la informacion de zona y/o grupo estan vacios
    def validarZonaOGrupoNan(self, hoja_leida,archivo , nombreHoja):
        error=""
        try:
            if hoja_leida.iloc[1,2] is None:
                error+="El dato del grupo está vacío"
            if isinstance(hoja_leida.iloc[1,2], str):
                error+="El dato del grupo esta incorrecto.\n"
            if hoja_leida.iloc[2,2] is None:
                error+="El dato de la zona está vacío.\n "
            if isinstance(hoja_leida.iloc[2,2], str):
                error+="El dato de la zona no contiene un numero sino un nombre.\n"
            if error!="":
                self.listaZonaOGrupoNan.append({"nombre_archivo": os.path.basename(archivo), "nombre_hoja": nombreHoja, "errores": error, "zona": hoja_leida.iloc[2,2], "grupo": hoja_leida.iloc[1,2] })
        except TypeError as e:
            print(str(e))
        

    #en esta funcion se llaman a todas las validacione,s optimizando su uso
    def validar(self, columna: dict):

        #Con el [1] especifico que es la posicion 1 de lo que devuelve la funcion validarColVacia(), en este caso true o false
        vacia = self.validarColVacia(columna)
        #si una columna esta vacia, no se valida nada
        if vacia[1]:
            return None
        else:
            
            caracteres = self.validarCaracteres(vacia[0])
            
            #si una columna contiene caracteres ya no se valida nada mas y se marcan todo el resto de errores como falsos
            if caracteres[1]:
                caracteres[0]["listaErrores"][2] = False
                caracteres[0]["listaErrores"][3] = False
                caracteres[0]["listaErrores"][4] = False
                caracteres[0]["listaErrores"][5] = False
                caracteres[0]["listaErrores"][6] = False
                caracteres[0]["listaErrores"][7] = False
                caracteres[0]["listaErrores"][8] = False
                caracteres[0]["listaErrores"][9] = False
                    
                return caracteres[0]
            else:
                #las columnas 53 y 54 corresponden a Vivienda de la cual no es necesario especificar tamanio, jornada
                #ni dias por lo cual solo se debe validar que no hayan caracteres
                if caracteres[0]["numColumna"]>=53:
                    
                    self.validarViviendas(caracteres[0])
                    return caracteres[0]
                else:
                
                    tamanio = self.validarTamanioDatosVacios(caracteres[0])
                    if tamanio[1]:
                        #si no hay datos en tamanio no es necesario realizar las otras validacions del tamanio, por lo cual
                        #se ponen las validaciones en False porque no presentaran ese error en concreto
                        tamanio[0]["listaErrores"][3] = False

                        caracteres[0] = tamanio[0]
                    else:
                        #verificar que la suma de los tamanios sea igual al numero de atractores
                        sumTamanio = self.validarSumaTamanio(tamanio[0])
                        caracteres[0] = sumTamanio[0]
                        try:
                            self.modificarCampoNAtractores(sumTamanio[0])
                        
                        except Exception as e:
                            print("\nNo se puede realizar la correccion de #Atractores porque el archivo esta dañado")

                    jornada = self.validarJornadaDatosVacios(caracteres[0])
                    if jornada[1]:
                        #si no hay datos en jornada no es necesario realizar las otras validacions de la jornada, por lo cual
                        #se ponen las validaciones en False porque no presentaran ese error en concreto
                        
                        jornada[0]["listaErrores"][5] = False
                        jornada[0]["listaErrores"][6] = False
                        col2 = jornada[0]
                    else:
                        col1 = self.validarSumaJornada(jornada[0])
                        col2 = self.validarJornadaNoSobrepaseAtractores(col1[0])[0]
                        
                        self.corregirDiurno(col2)
                        
                            

                    dias = self.validarDiasDatosVacios(col2)
                    if dias[1]:
                        #si no hay datos en dias no es necesario realizar las otras validacions de los dias, por lo cual
                        #se ponen las validaciones en False porque no presentaran ese error en concreto
                
                        dias[0]["listaErrores"][8] = False
                        dias[0]["listaErrores"][9] = False
                        colRetorno = dias[0]
                    else:
                        colDias = self.validarDiasNoSobrepaseAtractores(dias[0])
                        colRetorno = self.validarSumaDias(colDias[0])[0]
                        
                        self.corregirEntreSemana(colRetorno)
                        
                            
        return colRetorno