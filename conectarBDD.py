import pyodbc

def leerArchivo():
    archivo = open('leer.txt', 'r')
    return [i for i in archivo]


# Conecta a la base de datos
conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\aimbe\OneDrive\Desktop\Vinculacion.accdb" )

# Crea un cursor para ejecutar consultas
cursor = conn.cursor()

# Ejemplo de consulta
for i in leerArchivo():
    cursor.execute('INSERT INTO atractor (nombre) VALUES (?)', i)
    
conn.commit()
cursor.execute("SELECT * FROM atractor")
# Obtiene los resultados
results = cursor.fetchall()

# Recorre los resultados
for row in results:
    print(row)

# Cierra la conexión y el cursor
cursor.close()
conn.close()