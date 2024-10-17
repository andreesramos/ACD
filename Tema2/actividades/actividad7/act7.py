import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='1dam'
    )
    
    if conexion.is_connected():
        cursor=conexion.cursor()
        print("Iniciando la transaccion")
        
        sql_insert="""
            insert into ObrasArte (titulo, artista, fechaCreacion, tecnica, museo)
            values (%s, %s, %s, %s, %s)
        """
        datos_obras= ("Las Meninas", "mi abuelo", "ayer", "oleo", "su casa")
        cursor.execute(sql_insert, datos_obras)
        conexion.commit()
        print("Transaccion exitosa: Registro insertado correctamente")
except Error as e:
    print(f"Error en la transacción: {e}")
    if conexion:
        conexion.rollback()
        print("Se realizo rollback")
finally:
    if conexion and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexion cerrada")
