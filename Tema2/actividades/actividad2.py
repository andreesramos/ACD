import pymysql
from pymysql import MySQLError

conexion = pymysql.connect(
    host='localhost',
    user='usuario',
    password='usuario',
    database='1dam'
)
    
cursor=conexion.cursor()
cursor.execute("INSERT INTO ObrasArte (titulo, artista, fechaCreacion, tecnica, museo) VALUES (%s, %s, %s, %s, %s), ")
cursor.execute("SELECT * FROM ObrasArte")
for fila in cursor.fetchall():
    print(fila)
conexion.close()