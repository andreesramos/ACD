import time
import pymysql
from pymysql import MySQLError
import random

start_time = time.time()

try:

    conexion=pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        db='1dam'
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
        cursor.execute("INSERT INTO ObrasArte (titulo, artista, fechaCreacion, tecnica, museo) VALUES (%s, %s, %s, %s, %s)",
            (titulo, artista, fecha, tecnica, museo)
        )
except MySQLError as e:
    print(f"Error de conexion: {e}")
finally:
    if conexion is not None:
        conexion.close()



end_time = time.time()
print(f"Tiempo de inserción con pymysql: {end_time - start_time} segundos")