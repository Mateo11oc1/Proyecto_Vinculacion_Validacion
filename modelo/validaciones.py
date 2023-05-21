import os
import glob
import pandas
import time
import math
import logging
import openpyxl
import xlwings 
#Las validaciones devuelve un valor de true si es que la columna presenta el error especificado, caso contrario, devuelve false
#diccionario de errores:
#1. Se han ingresado caracteres o decimales
#2. En un atractor, hay datos de numero de atractores, jornada o dias pero los datos del tamanio estan vacios
#3. La suma de los tamanios no coincide con el numero de atractores
#4. En un atractor, hay datos de numero de atractores, tamanio o dias pero los datos de la jornada estan vacios
#5. La suma de los datos de la jornada es menor al numero de atractores
#Por ejemplo hay 3 atractores tipo Restaurante, se indica que hay 1 matutino y 1 nocturno, la suma de ambos es 2<al numero de atractores
#6. Hay uno o varios datos de la jornada que sobrepasa el numero de atractores
#Por ejemplo hay 3 atractores tipo Restaurante se indica que hay 4 diurnos lo cual es incorrecto
#7. En un atractor, hay datos de numero de atractores, tamanio o jornada pero los datos de los dias estan vacios
#8.Validar que uno o varios de los datos de los días de atención no sobrepasen el numero de atractores
#La validacion 8 es igual a la 6 pero corresponde a los dias de atencion
#9. Validar que la suma de todos los datos en dias no sea menor al numero de atractores
#La validacion 9 es igual a la 5 pero corresponde a los dias de atencion

class Validaciones:

    def __init__(self):
        
        # self.carpetaExcel = "../"
        self.archivos_excel = []
        self.workbook = None
        self.diccionarioErrores={1:"Se han ingresado caracteres\n", 2:"Hay datos de numero de atractores, jornada o dias pero los datos del tamanio estan vacios\n",
                        3:"La suma de los tamanios no coincide con el numero de atractores\n", 4:"Hay datos de numero de atractores, tamanio o dias pero los datos de la jornada estan vacios\n",
                        5: "La suma de los datos de la jornada es menor al numero de atractores\n", 6:"Hay uno o varios datos de la jornada que sobrepasa el numero de atractores\n",
                        7: "Hay datos de numero de atractores, tamanio o jornada pero los datos de los dias estan vacios\n", 8:"Uno o varios de los datos de los días de atención sobrepasan el numero de atractores\n",
                        9: "La suma de los datos de los dias es menor al numero de atractores\n"}
        self.contadorCorrecciones=0
        self.dataframe=pandas.read_excel("formato_archivos.xlsx", sheet_name="Hoja1")



    #Obtengo una lista de todos lo archivos excel
    def leerCarpeta(self, carpeta):
        # Obtener todos los archivos en la carpeta que tengan la extensión .xlsx
        self.archivos_excel = [archivo for archivo in  glob.glob(os.path.join(carpeta, '*.xlsx')) if not os.path.basename(archivo).startswith("~$")]
        

    #este metodo valida que las hojas tengan formato correcto retornando True si hay un error de formato
    #un error de formato es si la tabla esta movida hacia arriba, abajo, derecha o izquierda
    def validarFormatoIncorrecto(self, nombre_hoja, nombre_archivo, hoja_leida):
        try:
            if hoja_leida.iloc[1,1]=="Grupo:" and hoja_leida.iloc[2,1]=="Zona:" and hoja_leida.iloc[6,2]=="Educación" and hoja_leida.iloc[9,1]=="# Atractores":
                pass
            else:
                
                with open("hojas_formato_erroneo.log", "a") as archivo:
                    archivo.write("Error de formato en la hoja "+nombre_hoja+" del archivo "+os.path.basename(nombre_archivo)+"\n")
                return True
        except:
            with open("hojas_formato_erroneo.log", "a") as archivo:
                    archivo.write("Error de formato en la hoja "+nombre_hoja+" del archivo "+os.path.basename(nombre_archivo)+"\n")
            return True  

    #Devuelve la columna como un diccionario de acuerdo a los parametros
    #opcion es para ver si se quiere retornar las columnas con errores o los archivos con observaciones
    def leerColumna(self)->list:
        self.listaColumnas = []
        self.columnasConErrores = []
    
        #Recorro todos los archivos
        #print(self.archivos_excel)
        for i in self.archivos_excel:
            #Leo todas las hojas de una vez del documento
            numHoja = 0
            try:
                leido = pandas.read_excel(i, sheet_name = None)
                
                
            except Exception as e:
                
                print(f"Error al leer el archivo {i}")
                #time.sleep(5)
            
            #Recorro cada hoja
            for nombreHoja,j in leido.items():
                #i es cada archivo
                #j es cada hoja de cada archivo
                #si el formato de la hoja es incorrecto no se hacen las validaciones de las columnas 

                if self.validarFormatoIncorrecto(nombreHoja, i,j)==True:
                    pass
                else:
                #Recorro cada columna
                #shape[1] nos da el numero de columnas de la hoja
                    try:
                        for h in range(2, j.shape[1]):
                            #Desde la fila 7 en adelante porque alli empiezan los datos que interesan almacenar(nombre de atractor,
                            # numero,dias,jornada, tamanio)
                            lista = j.iloc[7:, h].values.tolist()
                            
                            columna = { "atractor": lista[0], "numAtractores":lista[2], "tamanio": lista[3:6], "jornada": lista[6:11],
                                    "dias": lista[12:22], "numColumna": h, "hoja": numHoja, "archivoRuta": i, "archivoNombre": os.path.basename(i), 
                                    "vacia":False, "listaErrores":{}, "grupo": j.iloc[1, 2], "zona":j.iloc[2, 2], "tramo": j.iloc[1, 12],
                                    "observaciones":j.iloc[30,1], "nombreHoja": nombreHoja}
                            #os.path.basename(i) es para q solo se escriba el nombre del archivo, no toda la ruta
                            
                            columna = self.validar(columna) #Se valida que la columna esta vacia al leer

                            if columna != None: #si la columna no esta vacia se agrega a la lista de columnas
                                print(f'---------\nArchivo: {columna["archivoNombre"]}\n Hoja: {columna["nombreHoja"]}\n Columna: {columna["numColumna"]}')
                                #print(columna)
                                self.listaColumnas.append(columna)
                                contador=0
                                for k in columna:
                                    for clave, valor in columna["listaErrores"].items():
                                    #si en listaErrores hay un valor del diccionario que contiene True(contiene un error) se agrega a la lista de columnas con errores
                                        if valor:
                                            contador+=1
                                            self.columnasConErrores.append(columna)
                                        
                                            break
                                        
                                    break
                        
                    except Exception as e:
                        print(f"Error en el archivo {os.path.basename(i)}. Hoja: {nombreHoja}: {e}")
                        #time.sleep(5)

                    numHoja += 1
            leido = None
            self.generarArchivoLog()
        return self.columnasConErrores
    


    
    def generarArchivoLog(self):
        
        cont=0
        cadenaEscribir = ""
        for i in self.columnasConErrores:
            iterador=0
            errores=""
            
            for valor in i["listaErrores"].values():
                iterador+=1
                if valor:
                    errores+=self.diccionarioErrores[iterador]
            cont+=1
            cadenaEscribir = (
                cadenaEscribir + str(cont)+"\n" + "Nombre del archivo: "+ str(i["archivoNombre"])+"\n" 
                + "Nombre de la hoja: " + str(i["nombreHoja"])+"\n" + "Atractor con problema: "
                + str(i["atractor"])+"\n" + "Errores: "+errores+"\n" + "Tramo: "+ str(i["tramo"])
                + "\n" + "Tramo: "+ str(i["tramo"])+"\n" + "Zona: "+ str(i["zona"])+"\n" + "Grupo: "+ 
                str(i["grupo"])+"\n" 
                + "------------------------------------------------------------------------------------------------------------\n"
                )
            
        with open("errores.log", "w") as archivo:
            cont+=1
            archivo.write(cadenaEscribir)
            archivo.close()
    

    def generarArchivoCorreccionesRealizadas(self, nombreCorreccion:str, columna):

        self.contadorCorrecciones+=1

        with open("correcciones.log", "a") as archivo:
            archivo.write(str(self.contadorCorrecciones)+"\n")
            archivo.write("Nombre del archivo: "+ str(columna["archivoNombre"])+"\n")
            archivo.write("Nombre de la hoja: "+ str(columna["nombreHoja"])+"\n")
            archivo.write("Correccion realizada: "+nombreCorreccion+"\n")
            archivo.write("Atractor corregido: "+ str(columna["atractor"])+"\n")
            archivo.write("----------------------------------------------------------------------------------------------------------------\n")
            archivo.close()


    def verObservacionesArchivos(self)->list:
        self.listaColumnas = []
        self.archivoConObservaciones = []
        #Recorro todos los archivos
        print(self.archivos_excel)
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
                try:
                    archivo={"hoja":numHoja, "archivoNombre":os.path.basename(i), "grupo": j.iloc[1, 2], "zona":j.iloc[2, 2], "tramo": j.iloc[1, 12],
                        "observaciones":j.iloc[30,1], "nombreHoja":nombreHoja}
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
            print("Corrigiendo numero de atractores...")
        
            # abrir el archivo
            print(columna["archivoRuta"])
                        
            # abre la aplicación de Excel en segundo plano
            app = xlwings.App(visible=False)
            
            # abrir el archivo
            wb = xlwings.Book(columna["archivoRuta"])

            # seleccionar la hoja
            hoja = wb.sheets[columna["nombreHoja"]]

            # modificar el valor de una celda
            hoja.cells(11, columna["numColumna"]+1).value = sum(x for x in columna['tamanio'] if not math.isnan(x))

            # guarda los cambios y cierra excel
            wb.save()
            wb.close()
            app.quit()

            self.generarArchivoCorreccionesRealizadas("Se ha escrito el numero de atractores en #Atractores", columna)

            



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
    def validarSumaJornada(self, columna:dict) -> list:

        #si el numero de atractores es mayor a la suma de los valores del jornada
        if columna["numAtractores"] > sum(x for x in columna['jornada'] if not math.isnan(x)):
            columna["listaErrores"][5] = True
            return [columna, True] #si hay el error
        else:
            columna["listaErrores"][5] = False
            return [columna, False] #no hay el error


    #Validar que uno o varios de los datos de la jornada no sobrepase el numero de atractores
    #No se valida que esto se cumpla con la suma de los datos de la jornada debido a que se puede tener un atractor
    #que sea matutino y nocturno a la vez
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
                print("Corrigiendo diurno...")
                # abrir el archivo
                print(columna["archivoRuta"])

                # abre la aplicación de Excel en segundo plano
                app = xlwings.App(visible=False)

                # abrir el archivo
                wb = xlwings.Book(columna["archivoRuta"])

                # seleccionar la hoja
                hoja = wb.sheets[columna["nombreHoja"]]

                # modificar el valor de una celda
                hoja.cells(17, columna["numColumna"]+1).value = sum(x for x in columna['tamanio'] if not math.isnan(x))
                hoja.cells(15, columna["numColumna"]+1).value = ""
                hoja.cells(16, columna["numColumna"]+1).value = ""

                # guarda los cambios y cierra excel
                wb.save()
                wb.close()
                app.quit()

                self.generarArchivoCorreccionesRealizadas("Se ha cambiado los datos de #vespertino y #matutino por #diurno", columna)

            
                
            
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
                print("Corrigiendo entre semana...")
                # abrir el archivo
                print(columna["archivoRuta"])
                            
                # abre la aplicación de Excel en segundo plano
                app = xlwings.App(visible=False)
                
                # abrir el archivo
                wb = xlwings.Book(columna["archivoRuta"])

                # seleccionar la hoja
                hoja = wb.sheets[columna["nombreHoja"]]

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

                self.generarArchivoCorreccionesRealizadas("Se ha cambiado #lunes, #martes, #miercoles, #jueves, #viernes por #entre semana", columna)

    #en esta funcion se llaman a todas las validacione,s optimizando su uso
    def validar(self, columna: dict):

        #Con el [1] especifico que es la posicion 1 de lo que devuelve la funcion validarColVacia(), en este caso true o false
        vacia = self.validarColVacia(columna)
        #si una columna esta vacia, no se valida nada
        if vacia[1]:
            return
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
                        self.modificarCampoNAtractores(sumTamanio[0])


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
                        self.corregirDiurno(col2) #Se comento porque es muy demorado
                    

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



