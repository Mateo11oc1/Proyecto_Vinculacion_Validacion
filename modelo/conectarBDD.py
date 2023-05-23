import pyodbc

class ConexionBDD():
    
    def __init__(self):
        self.conectar()
    
    
    def conectar(self):
        # Conecta a la base de datos
        self.conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=..\Vinculacion.accdb")

        # Crea un cursor para ejecutar consultas
        self.cursor = self.conn.cursor()
    
    def insertarColumna(colimna:dict):
        pass