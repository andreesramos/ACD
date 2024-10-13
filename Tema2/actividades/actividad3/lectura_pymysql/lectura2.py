import time
import pymysql
from pymysql import MySQLError

start_time = time.time()

try:
    conexion=pymysql.connect(
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
        cursor.fetchall()

    end_time = time.time()
    print(f"Tiempo de lectura con pymysql: {end_time - start_time} segundos")
except MySQLError as e:
    print(f"Error de conexion: {e}")
finally:
    if conexion is not None:
        conexion.close()