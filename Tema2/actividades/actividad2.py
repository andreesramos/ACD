import pymysql
from pymysql import MySQLError

conexion = pymysql.connect(
    host='localhost',
    user='usuario',
    password='usuario',
    database='1dam'
)
    
cursor=conexion.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ObrasArte(
        titulo varchar(20) primary key,
        artista varchar(30),
        fechaCreacion varchar(10),
        tecnica varchar(15),
        museo varchar(15)
    )
""")

cursor.execute(
    "INSERT INTO ObrasArte (titulo, artista, fechaCreacion, tecnica, museo) VALUES (%s, %s, %s, %s, %s)",
    ("La ultima cena", "Leonardo da Vinci", "1495", "Oleo temple", "Santa Maria")
)
conexion.commit()

cursor.execute("SELECT * FROM ObrasArte")
for fila in cursor.fetchall():
    print(fila)
conexion.close()