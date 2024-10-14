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
    "delete from ObrasArte where fechaCreacion<%s", (1600)
)

conexion.commit()
print("Registros borrados")
conexion.close()