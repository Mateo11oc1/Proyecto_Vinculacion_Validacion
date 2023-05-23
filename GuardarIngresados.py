
import pickle
import pandas
# Deserializar el objeto desde el archivo
with open('datos.dat', 'rb') as archivo:
    datos = pickle.load(archivo)

    
print(len(datos))  # Imprimir el objeto deserializado
