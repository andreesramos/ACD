import pymysql
from pymysql import MySQLError

conexion=pymysql.connect(
    host='localhost',
    user='usuario',
    password='usuario',
    database='1dam'
)

cursor=conexion.cursor()
cursor.execute(
    "update ObrasArte set fechaCreacion=%s where titulo=%s", (1505, "La Gioconda")
)

conexion.commit()
print("Registro actualizado")
conexion.close()