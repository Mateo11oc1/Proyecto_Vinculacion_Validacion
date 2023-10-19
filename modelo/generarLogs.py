class GenerarLogs:
    def __init__(self):
        self.diccionarioErrores={1:"Se han ingresado caracteres\n", 2:"Hay datos de numero de atractores, jornada o dias pero los datos del tamanio estan vacios\n",
                        3:"La suma de los tamanios no coincide con el numero de atractores\n", 4:"Hay datos de numero de atractores, tamanio o dias pero los datos de la jornada estan vacios\n",
                        5: "La suma de los datos de la jornada es menor al numero de atractores\n", 6:"Hay uno o varios datos de la jornada que sobrepasa el numero de atractores\n",
                        7: "Hay datos de numero de atractores, tamanio o jornada pero los datos de los dias estan vacios\n", 8:"Uno o varios de los datos de los días de atención sobrepasan el numero de atractores\n",
                        9: "La suma de los datos de los dias es menor al numero de atractores\n"} 
    
    def generarArchivosLog(self, columnasConErrores, listaFormatoIncorrecto, hojasConCallesInvalidas, listaZonaOGrupoMal):
        self.generarArchivoErrores(columnasConErrores)
        self.generarArchivoCallesNoReconocidas(hojasConCallesInvalidas)
        self.generarArchivoFormatoIncorrecto(listaFormatoIncorrecto)
        self.generarArchivoZonaGrupoIncorrecto(listaZonaOGrupoMal)

    def generarArchivoCallesNoReconocidas(self, hojasConCallesInvalidas):
        #metodo que genera un archivo log detallando archivo y hoja de las calles no reconocidas
        cont=0

        cadenaEscribir = ""
        for calle in hojasConCallesInvalidas:
            cont+=1
            cadenaEscribir = (
                cadenaEscribir + str(cont)+"\n" + "Nombre del archivo: "+ str(calle["nombre_archivo"])+"\n" 
                + "Nombre de la hoja: " + str(calle["nombre_hoja"])+"\n" + "Calle: "
                + str(calle["calle"])+"\n" + "Tipo calle: "+str(calle["tipo"]) +"\n"
                + "------------------------------------------------------------------------------------------------------------\n"
                )  

        with open("log/callesInvalidas.log", "w",  encoding="utf-8") as archivo:
            archivo.write(cadenaEscribir)
            archivo.close()
    
    def generarArchivoErrores(self, columnasConErrores):
        
        cont=0
        cadenaEscribir = ""
        for i in columnasConErrores:
            iterador=0
            errores=""
            
            for valor in i["listaErrores"].values():
                iterador+=1
                if valor:
                    errores+=self.diccionarioErrores[iterador]
            cont+=1
            cadenaEscribir = (
                cadenaEscribir + str(cont)+"\n" + "Nombre del archivo: "+ str(i["nombre_archivo"])+"\n" 
                + "Nombre de la hoja: " + str(i["nombre_hoja"])+"\n" + "Atractor con problema: "
                + str(i["atractor"])+"\n" + "Errores: "+errores+"\n" + "Tramo: "+ str(i["tramo"])
                + "\n" + "Tramo: "+ str(i["tramo"])+"\n" + "Zona: "+ str(i["zona"])+"\n" + "Grupo: "+ 
                str(i["grupo"])+"\n" 
                + "------------------------------------------------------------------------------------------------------------\n"
                )
            
        with open("log/errores.log", "w",  encoding="utf-8") as archivo:
            cont+=1
            archivo.write(cadenaEscribir)
            archivo.close()

    def generarArchivoCorreccionesRealizadas(self, nombreCorreccion:str, columna, contador):

        with open("log/correcciones.log", "a",  encoding="utf-8") as archivo:

            archivo.write(str(contador)+"\n")
            archivo.write("Nombre del archivo: "+ str(columna["nombre_archivo"])+"\n")
            archivo.write("Nombre de la hoja: "+ str(columna["nombre_hoja"])+"\n")
            archivo.write("Correccion realizada: "+nombreCorreccion+"\n")
            archivo.write("Atractor corregido: "+ str(columna["atractor"])+"\n")
            archivo.write("----------------------------------------------------------------------------------------------------------------\n")
            archivo.close()

    def generarArchivoFormatoIncorrecto(self, hojasConFormatoIncorrecto):

        cont=0

        cadenaEscribir = ""
        for hoja in hojasConFormatoIncorrecto:
            cont+=1
            cadenaEscribir = (
                cadenaEscribir + str(cont)+"\n" + "Nombre del archivo: "+ str(hoja["nombre_archivo"])+"\n" 
                + "Nombre de la hoja: " + str(hoja["nombre_hoja"])+"\n" 
                + "------------------------------------------------------------------------------------------------------------\n"
                )  

        with open("log/formatoIncorrecto.log", "w",  encoding="utf-8") as archivo:
            archivo.write(cadenaEscribir)
            archivo.close()

    def generarArchivoZonaGrupoIncorrecto(self, zonaGrupoIncorrecto):

        cont=0

        cadenaEscribir = ""
        for hoja in zonaGrupoIncorrecto:
            cont+=1
            cadenaEscribir = (
                cadenaEscribir + str(cont)+"\n" + "Nombre del archivo: "+ str(hoja["nombre_archivo"])+"\n" 
                + "Nombre de la hoja: " + str(hoja["nombre_hoja"])
                +"Errores:" + str(hoja["errores"])+"\n" 
                +"Zona:" + str(hoja["zona"])+"\n" 
                +"Grupo:" + str(hoja["grupo"])+"\n" 
                + "------------------------------------------------------------------------------------------------------------\n"
                )  

        with open("log/zonaGrupoIncorrecto.log", "w",  encoding="utf-8") as archivo:
            archivo.write(cadenaEscribir)
            archivo.close()