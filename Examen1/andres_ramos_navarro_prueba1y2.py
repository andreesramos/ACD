import json, csv, mysql.connector
from mysql.connector import Error
from pathlib import Path

class FileManager:
    #Funcion para leer el archivo .txt
    def read_file(self, file_path, mode='r'):
        try:
            with open(file_path, mode) as archivo:
                content=archivo.read()
        except Exception as e:
            print("Error leyendo el archivo: {e}")
            
class CSVFileHandler:
    #Funcion para leer el archivo csv
    def read_csv(self, file_path):
        try:
            with open(file_path, mode='r', newline='') as f:
                reader = csv.DictReader(f) 
            rows = [] 
            for row in reader:
                rows.append(row)
            print("Leyendo datos desde el csv")
            return rows
        except Exception as e:
            print(f"Error leyendo el archivo CSV: {e}")
            
class JSONFileHandler:
    #Funcion para leer el archivo json
    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
            print("Leyendo datos desde el json")
        except Exception as e:
            print(f"Error leyendo JSON: {e}")

def leer_csv():
    archivo='libros_unamuno.csv'
    contenido_csv=CSVFileHandler.read_csv(CSVFileHandler, archivo)
    return contenido_csv

def leer_json():
    archivo='libros_machado.json'
    contenido_json=JSONFileHandler.read_json(JSONFileHandler, archivo)
    return contenido_json



#Conexion a la base de datos
try:
    conexion = mysql.connector.connect(
    host='localhost',
    user='usuario',
    password='usuario',
    database='1dam'
    )
    if conexion.is_connected():
        print("Conexion a la base de datos exitosa")
except Error as e:
    print(f"Error de conexion: {e}")

#Creacion de la tabla
cursor=conexion.cursor()
try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Libros(
        id int primary key,
        titulo varchar(50),
        autor varchar(50),
        genero varchar(50),
        año_publicacion int,
        libreria_origen varchar(50)
    )
    """)
    conexion.commit()
    print("Creando la tabla 'Libros' en la base de datos...")
except Error as e:
    print(f"Error al crear la tabla: {e}")

#Lectura del fichero
file_manager=FileManager()
file_manager.read_file("libros_valle_inclan.txt")

#Insercion de datos originales
try:
    cursor.execute(
        "INSERT INTO Libros (id, titulo, autor, genero, año_publicacion, libreria_origen) values (%d, %s, %s, %s, %d, %s)",
        (1, "Don Quijote de la Mancha", "Miguel de Cervantes", "Novela", 1605, "Ramón Valle Inclán")
    )
    cursor.execute(
        "INSERT INTO Libros (id, titulo, autor, genero, año_publicacion, libreria_origen) values (%d, %s, %s, %s, %d, %s)",
        (2, "Cien Años de Soledad", "Gabriel García Márquez", "Novela", 1967, "Ramón Valle Inclán")
    )
    cursor.execute(
        "INSERT INTO Libros (id, titulo, autor, genero, año_publicacion, libreria_origen) values (%d, %s, %s, %s, %d, %s)",
        (3, "Crimen y Castigo", "Fiódor Dostoyevski", "Novela", 1866, "Ramón Valle Inclán")
    )
    cursor.execute(
        "INSERT INTO Libros (id, titulo, autor, genero, año_publicacion, libreria_origen) values (%d, %s, %s, %s, %d, %s)",
        (4, "La Casa de los Espíritus", "Isabel Allende", "Novela", 1982, "Ramón Valle Inclán")
    )
    cursor.execute(
        "INSERT INTO Libros (id, titulo, autor, genero, año_publicacion, libreria_origen) values (%d, %s, %s, %s, %d, %s)",
        (5, "El Nombre de la Rosa", "Umberto Eco", "Misterio", 1980, "Ramón Valle Inclán")
    )
    conexion.commit()
    print("Insertando los libros originales de la Librería Ramón Valle Inclán...")
except Error as e:
    print(f"Error al insertar los datos: {e}")

leer_csv()
leer_json()

insert_file="""
        INSERT INTO Libros (titulo, autor, genero, año_publicacion, libreria_origen)
        VALUES (%s, %s, %s, %d, %s)
    """

try:
    cursor.execute(insert_file, leer_csv)
    print("Iniciando transacción para insertar libros en la base de datos...")
    conexion.commit()
    print("Transacción completada: Todos los libros insertados con éxito.")
except Error as e:
    conexion.rollback()
    