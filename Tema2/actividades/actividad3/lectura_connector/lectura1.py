import time
import mysql.connector
from mysql.connector import Error

start_time = time.time()

try:
    conexion=mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        db='1dam'
        )
    cursor=conexion.cursor()

    for i in range(0, 10000):
        cursor.execute(
            "SELECT * FROM ObrasArte;"
        )

    end_time = time.time()
    print(f"Tiempo de lectura con mysql-connector: {end_time - start_time} segundos")
except Error as e:
    print(f"Error de conexion: {e}")
finally:
    if conexion is not None:
        conexion.close()
