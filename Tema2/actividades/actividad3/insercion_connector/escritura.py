import time
import mysql.connector
from mysql.connector import Error
import random

start_time = time.time()

try:
    conexion=mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='1dam'
        )
    cursor=conexion.cursor()

    artista=['Manolo', 'Pepe', 'Antonio', 'Pablo']
    fecha=['1996', '1721', '1608', '1833']
    tecnica=['oleo', 'sfumato', 'alla prima', 'acuarela']
    museo=['prado', 'louvre', 'britanico', 'moma']

    for i in range(0, 10000):
        titulo = f"Obra {i+1}"
        artista = random.choice(artista)
        fecha = random.choice(fecha)
        tecnica = random.choice(tecnica)
        museo = random.choice(museo)
        cursor.execute(
            "INSERT INTO ObrasArte (titulo, artista, fechaCreacion, tecnica, museo) VALUES (%s, %s, %s, %s, %s)",
            (titulo, artista, fecha, tecnica, museo)
        )

    end_time = time.time()
    print(f"Tiempo de inserción con mysql-connector: {end_time - start_time} segundos")
except Error as e:
    print(f"Error de conexion: {e}")
finally:
    if conexion.is_connected():
        conexion.close()

