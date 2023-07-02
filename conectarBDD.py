import pyodbc

def leerArchivo():
    archivo = open('leer.txt', 'r')
    return [i for i in archivo]


# Conecta a la base de datos
#(r"DRIVER..."")-> es para ignorar \n \t
conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./Vinculacion.accdb" )

# Crea un cursor para ejecutar consultas
cursor = conn.cursor()

# Ejemplo de consulta
cursor.execute("delete from tramo")
cursor.execute("delete from horario")
cursor.execute("delete from jornada")
cursor.execute("delete from tamanio")
cursor.execute("delete from tramo_atractor_caracteristica")
# cursor.execute("SELECT * FROM calle WHERE nombre LIKE ?", "AGUSTIN CUEVA VALLEJO")

# for i in range(1, 53):
#     cursor.execute("INSERT INTO motivoAtraccion_atractor (idMotivoAtraccion, idTipoAtractor) VALUES (?, ?)",(1, i) )
# # res = cursor.fetchall()

# print(res)
conn.commit()

# Cierra la conexión y el cursor
cursor.close()
conn.close()