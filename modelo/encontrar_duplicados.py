
def encontrar_duplicados(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
        
    lineas = contenido.split('\n')
    elementos = []
    duplicados = []
    
    for linea in lineas:
        if linea:
            elementos.append(linea)
            if elementos.count(linea) > 1 and linea not in duplicados:
                duplicados.append(linea)
    
    no_duplicados = sorted(list(set(elementos) - set(duplicados)))
    
    return duplicados, no_duplicados


# Ejemplo de uso
nombre_archivo = 'callesBDD.log'
duplicados, no_duplicados = encontrar_duplicados(nombre_archivo)

#print("Elementos duplicados encontrados:")
#print(duplicados)

print("Elementos no duplicados ordenados alfabéticamente:")
for i in no_duplicados:

    with open("callesBDD_sin_duplicados.log", 'a') as archivo:
        archivo.write(str(i)+"\n")
        

