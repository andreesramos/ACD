import pymysql
from pymysql import MySQLError
try:
    conexion = pymysql.connect(
    host='localhost',
    user='usuario',
    password='usuario',
    database='1dam'
    )
    if conexion is not None:
        print("Conexión a la base de datos exitosa")
except MySQLError as e:
    print(f"Error de conexión: {e}")
finally:
    if conexion is not None:
        conexion.close()
    print("Conexión cerrada")