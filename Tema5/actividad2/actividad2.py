from pymongo import MongoClient, errors

#Datos para la conexion
usuario = "usuario"
clave = "usuario"
base_datos = "1dam"
host = "localhost"
puerto = "27017"

try:
    #Conexion al servidor MongoDB
    client = MongoClient(f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}", 
    serverSelectionTimeoutMS=5000)

    #Seleccion de la base de datos
    db = client[base_datos]

    #Acceso a la base de datos para verificar la conexion
    colecciones = db.list_collection_names()
    print("Conexion exitosa. Colecciones en la base de datos: ")

    #Seleccion de la coleccion
    coleccion_usuarios=db["ObrasArte"]

    print("Consulta 1:")
    #Consulta donde autor sea igual a "Leonardo da Vinci"
    consulta={"artista": "Leonardo da Vinci"}
    usuarios=coleccion_usuarios.find(consulta)
    #Impresion de usuarios que cumplen la condicion
    for usuario in usuarios:
        print(usuario)

    print("\nConsulta 2:")
    #Seleccion de algunos campos especificos
    proyeccion={"titulo": 1, "artista": 1, "_id": 0}
    usuarios=coleccion_usuarios.find(consulta, proyeccion)
    for usuario in usuarios:
        print(usuario)

    print("\nConsulta 3:")
    usuarios=coleccion_usuarios.find(consulta, proyeccion).limit(2).sort("titulo")
    for usuario in usuarios:
        print(usuario)

except errors.ServerSelectionTimeoutError as err:
    #Error si no se puede conectar el servidor
    print(f"No se pudo conectar a MongoDB: {err}")
except errors.OperationFailure as err:
    #Error si las credenciales no son correctas o por falta de permisos
    print(f"Fallo en la autenticacion o permisos insuficientes: {err}")
except Exception as err:
    #Cualquier otro error
    print(f"Ocurrio un error inesperado: {err}")
finally:
    #Cierre de la conexion
    if 'client' in locals():
        client.close()
        print("\nConexion cerrada")