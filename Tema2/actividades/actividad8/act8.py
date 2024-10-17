import mysql.connector

conexion=mysql.connector.connect(
    host='localhost',
    user='usuario',
    password='usuario',
    database='1dam'
)

cursor=conexion.cursor()

cursor.callproc("contar_obras", ("Oleo",))
for resultado in cursor.stored_results():
    print(resultado.fetchall())

cursor.close()
conexion.close()
