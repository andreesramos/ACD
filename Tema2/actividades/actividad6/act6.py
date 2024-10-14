import pymysql

conexion=pymysql.connect(
    host='localhost',
    user='usuario',
    password='usuario',
    database='1dam'
)

cursor1=conexion.cursor()
cursor1.execute(
    "select * from ObrasArte"
)

for i in range(1, 6):
    primera=cursor1.fetchone()
    print(primera)
cursor1.close()

cursor2=conexion.cursor()
cursor2.execute(
    "select * from ObrasArte"
)

for i in range(1, 6):
    segunda=cursor2.fetchone()
    print(segunda)
cursor2.close()

conexion.close()