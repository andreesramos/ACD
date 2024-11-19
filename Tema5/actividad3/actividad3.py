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
    print("Conexion exitosa. ")

    #Seleccion de la coleccion
    coleccion_obras=db["ObrasArte"]

    #Definir varios documentos
    obrasArte=[
        {"titulo": "El nacimiento de Venus", "artista": "Sandro Botticelli", "museo": "Galeria Uffizi"},
        {"titulo": "El Grito", "artista": "Edvard Munch", "museo": "Museo Munch"},
        {"titulo": "El beso", "artista": "Gustav Klimt", "museo": "Palacio Belvedere"}
    ]
    #Insercion de los documentos en la coleccion
    resultado=coleccion_obras.insert_many(obrasArte)
    print("Insercion exitosa")
    
    #Actualizar un documento
    resultado=coleccion_obras.update_one(
        {"titulo": "El beso"},
        {"$set": {"museo": "Belvedere"}}
    )

    #Verificar el exito de la modificacion
    if resultado.modified_count > 0:
        print("Documento modificado con exito")
    else:
        print("No se encontro el documento o no hubo cambios")
    
    #Eliminacion de un documento
    resultado=coleccion_obras.delete_one({"titulo": "El Grito"})
    #Verificar el exito de la eliminacion
    if resultado.deleted_count > 0:
        print("Documento eliminado con exito")
    else:
        print("No se encontro el documento para eliminar")      
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