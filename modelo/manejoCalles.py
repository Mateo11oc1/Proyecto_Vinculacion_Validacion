import re
from tenacity import retry, stop_after_attempt, wait_fixed
from unidecode import unidecode
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from modelo.OperacionesBDD import BaseDatos
class ManejoCalles:
    def __init__(self):
        self.baseDatos=BaseDatos()
        self.hojasConCallesInvalidas=[]
        self.callesNoConectadas = [] #almacena las calles que han sobrepasado el tiempo de conexion con la API para igual validarlas al final del programa
        self.callesValidas=[]
        self.calles_tramos = []

    def almacenarCalles_Tramo(self, hoja, nombre_archivo, nombre_hoja):
        calles_secundarias=str(hoja.iloc[3,14])
        # Eliminar la cadena "S/N" de calles_secundarias porque / es un separador de calles y podria confundir a N como una calle y a S como otra
        calles_secundarias = calles_secundarias.replace("S/N", "")
        #para separar las calles se consideran los siguientes separadores
        # si hay una  " y ", " Y " , " entre ", " Entre ", "e", "E", "ENTRE" que separe las calles
        # separaciones por guiones -, por amperson &, por slash /
        #separar por numeros con punto 1. 2. o numero seguido de ) 1) 2)
        separadores=[r'\by\b',r'\be\b',r'\bE\b', r'\bENTRE\b', r'\s*,\s*', r'\s*-\s*', r'\s*&\s*',  r'\d\.', r'\s*/\s*', r'\bentre\b', r'\bY\b', r'\d+\)', r'\bEntre\b']
        patron='|'.join(separadores) #une los separadores para dividir las calles si se cumple cualquier a de los patrones especificados 
        #patron contiene \by\b|\s*,\s*|\s*-\s*|\s*&\s*|\d\.|\s*\/\s*
        calles = [] 
        #si es que no esta vacia la celda de calles secundarias 
        if calles_secundarias!=None:
            calles=re.split(patron, str(calles_secundarias))
            # Eliminar espacios en blanco al inicio y al final de cada calle
            calles = [calle.strip() for calle in calles if calle and calle.strip()]  
            
            return {"calle principal":str(hoja.iloc[2,12]), "calles secundarias": calles, "tramo": hoja.iloc[1,12], "nombre_hoja": nombre_hoja, "nombre_archivo": nombre_archivo}
    
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
    def buscar_direccion(self, direccion, diccionarioCalles, tipo): #tipo es el tipo de calle
        try:
            geolocator = Nominatim(user_agent="proyecto_vinculacion")  # Especifica un nombre de agente personalizado
            location = geolocator.geocode(direccion + ', Cuenca, Ecuador')
            return location
        except GeocoderTimedOut as e:
            print("Problema de GeocoderTimedOut: "+direccion+"\n")
            print(e)
            no_conectada={"nombre_archivo": diccionarioCalles["nombre_archivo"], "nombre_hoja": diccionarioCalles["nombre_hoja"], "calle": direccion, "tipo": tipo}
            self.callesNoConectadas.append(no_conectada)
            return "problema_conexion"
        except GeocoderUnavailable as e:
            print("Problema de GeocoderUnavailable en la calle: "+direccion+"\n")
            print(e)
            no_conectada={"nombre_archivo": diccionarioCalles["nombre_archivo"], "nombre_hoja": diccionarioCalles["nombre_hoja"], "calle": direccion, "tipo":tipo}
            self.callesNoConectadas.append(no_conectada)
            
            return "problema_conexion"

    def compararCalles(self, callesTramo: dict):
        
        def buscarCallesSecundarias(listaSecundarias: list,diccionarioCalles):
            
            sec_validas = []
            for secundaria in listaSecundarias:
                location = self.buscar_direccion(secundaria, diccionarioCalles, "secundaria")
                if location is not None and location!="problema_conexion":
                    print("Calle secundaria: ", secundaria)
                    print('Calle de API:', location.address)
                    print('Latitud:', location.latitude)
                    print('Longitud:', location.longitude)
                    calle_bien={"nombre_archivo": callesTramo["nombre_archivo"], "nombre_hoja": callesTramo["nombre_hoja"], "calle": secundaria, "tipo": "secundaria"}
                    calleEncontrada = self.baseDatos.buscarCalleBDD(location.address.split(",")[0].strip())
                    if calleEncontrada:
                        sec_validas.append(calleEncontrada)
                    else:
                        self.baseDatos.ingresarCalle(unidecode(str.upper(location.address.split(",")[0].strip())))
                        sec_validas.append(self.baseDatos.buscarCalleBDD(location.address.split(",")[0].strip()))
                    self.callesValidas.append(calle_bien)
                
                elif location == "problema_conexion":
                    print("Calle secundaria sin conectarse: ", secundaria)
                    sec_validas.append(["",""])
                else:
                    print('No se encontró la calle '+secundaria)
                    calle_mal={"nombre_archivo": callesTramo["nombre_archivo"], "nombre_hoja": callesTramo["nombre_hoja"], "calle": secundaria, "tipo": "secundaria"}
                    self.hojasConCallesInvalidas.append(calle_mal)
                    sec_validas.append(["",""])
            
            return sec_validas
        #------------------------------------------------------------------------------------------------------------------------------------------

        location = self.buscar_direccion(callesTramo["calle principal"], callesTramo, "principal")
    
        if location is not None and location!="problema_conexion":
            print("Calle principal: ", callesTramo["calle principal"])
            print('Calle de API:', location.address)
            print('Latitud:', location.latitude)
            print('Longitud:', location.longitude)
            prin_valida = self.baseDatos.buscarCalleBDD(location.address.split(",")[0].strip())
            if prin_valida:
                self.baseDatos.ingresarCalle(unidecode(str.upper(location.address.split(",")[0].strip())))
                prin_valida = self.baseDatos.buscarCalleBDD(location.address.split(",")[0].strip())
                
            calle_bien={"nombre_archivo": callesTramo["nombre_archivo"], "nombre_hoja": callesTramo["nombre_hoja"], "calle":callesTramo["calle principal"], "tipo": "secundaria"}
            self.callesValidas.append(calle_bien)
        elif location == "problema_conexion":
            print("Calle principal sin conectarse: ", callesTramo["calle principal"])
            prin_valida = ["",""]
        else:
            print('No se encontró la calle '+callesTramo["calle principal"])
            calle_mal={"nombre_archivo": callesTramo["nombre_archivo"], "nombre_hoja": callesTramo["nombre_hoja"], "calle": callesTramo["calle principal"], "tipo": "principal"}
            self.hojasConCallesInvalidas.append(calle_mal)
            prin_valida = ["",""]
        
        return {"principal": prin_valida, "secundarias":buscarCallesSecundarias(callesTramo["calles secundarias"], callesTramo)}
        
    def reintentarConectarCalles(self):
        print("Calles no conectadas"+str(self.callesNoConectadas))
        #hacer una copia de la lista para luego vaciarla 
        self.copia=self.callesNoConectadas.copy()
        self.callesNoConectadas=[] #no vaciarle antes ojo
        #volver a intentar conectar las calles
        
        for no_conectada in self.copia:
            location=self.buscar_direccion(no_conectada["calle"], no_conectada, no_conectada["tipo"])
            if location is not None and location!="problema_conexion":
                print("Calle: ", no_conectada["calle"])
                print('Calle de API:', location.address)
                print('Latitud:', location.latitude)
                print('Longitud:', location.longitude)
                calle_bien={"nombre_archivo": no_conectada["nombre_archivo"], "nombre_hoja": no_conectada["nombre_hoja"], "calle": no_conectada["calle"], "tipo": no_conectada["tipo"]}
                self.callesValidas.append(calle_bien)
            elif location == "problema_conexion":
                pass
            else:
                print("La calle "+no_conectada["calle"]+" no existe")
                calle_mal={"nombre_archivo": no_conectada["nombre_archivo"], "nombre_hoja": no_conectada["nombre_hoja"], "calle": no_conectada["calle"], "tipo": no_conectada["tipo"]}
                self.hojasConCallesInvalidas.append(calle_mal)
        
        self.hojasConCallesInvalidas.extend(self.copia)
        
        print("Calles no conectadas parte 2 "+str(self.copia))

