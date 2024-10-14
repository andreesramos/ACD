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
    create table if not exists Museos (
        id int primary key,
        nombre varchar (50),
        ubicacion varchar(50)
    )
""")

cursor.execute(
    "alter table ObrasArte add museo_id int, add constraint fk_museo foreign key (museo_id) references Museos(id)"
)
 
print("Relación de tablas ObrasArte y Museos creada correctamente")
conexion.close()