import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError

class ProductoManager:
    def __init__(self, database_name, collection_name):
        """Inicializa el componente ProductoManager."""
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self.uri = None

    def conectar(self):
        """Conectar a la base de datos MongoDB"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            logging.info(f"Conectado a MongoDB: {self.database_name}.{self.collection_name}")
        except PyMongoError as e:
            logging.error(f"Error al conectar a MongoDB: {e}")

    def cerrar_conexion(self):
        """Cerrar la conexión a MongoDB"""
        if self.client:
            self.client.close()
            logging.info("Conexión a MongoDB cerrada.")

    def insertar_productos(self, productos):
        """Insertar nuevos productos en la colección"""
        try:
            result = self.collection.insert_many(productos)
            logging.info("Documentos insertados exitosamente")
            return result
        except PyMongoError as e:
            logging.error(f"Error al insertar el documento: {e}")
            
    def consultar_proyeccion_ordenada(self, filtro, proyeccion, orden):
        try:
            productos = list(self.collection.find(filtro, proyeccion).sort(orden, -1))
            logging.info(f"Productos recuperados: {len(productos)}")
            for prod in productos:
                logging.info(prod)
            return productos
        except PyMongoError as e:
            logging.error(f"Error al mostrar los productos: {e}")
            

    def mostrar_todos_productos(self):
        """Mostrar todos los productos"""
        try:
            productos = list(self.collection.find())
            logging.info(f"Productos recuperados: {len(productos)}")
            for prod in productos:
                logging.info(prod)
            return productos
        except PyMongoError as e:
            logging.error(f"Error al mostrar los productos: {e}")
            

    def actualizar_productos(self, filtro, actualizacion):
        """Actualizar un producto en la colección"""
        try:
            result = self.collection.update_many(filtro, {"$set": actualizacion})
            if result.modified_count > 0:
                logging.info(f"Productos actualizados exitosamente")
            else:
                logging.warning(f"No se encontró producto para actualizar: {filtro}")
        except PyMongoError as e:
            logging.error(f"Error al actualizar el producto: {e}")
            
    def contar_documentos(self):
        try:
            result = self.collection.count_documents({})
            logging.info(f"Numero de documentos: {result}")
            return result
        except PyMongoError as e:
            logging.error(f"Error al contar los documentos: {e}")

    def eliminar_documentos(self, filtro):
        """Eliminar un documento de la colección"""
        try:
            result = self.collection.delete_many(filtro)
            if result.deleted_count > 0:
                logging.info(f"Productos eliminados exitosamente")
            else:
                logging.warning(f"No se encontró documento para eliminar: {filtro}")
        except PyMongoError as e:
            logging.error(f"Error al eliminar el documento: {e}")
            
    def consulta_compleja(self, filtro, proyeccion, orden):
        try:
            productos = list(self.collection.find(filtro, proyeccion).sort(orden))
            logging.info(f"Productos recuperados: {len(productos)}")
            for prod in productos:
                logging.info(prod)
            return productos
        except PyMongoError as e:
            logging.error(f"Error al mostrar los productos: {e}")
        

    def iniciar_transaccion(self):
        """Iniciar una transacción"""
        try:
            self.session = self.client.start_session()
            self.session.start_transaction()
            logging.info("Transacción iniciada.")
        except PyMongoError as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirmar (commit) una transacción"""
        try:
            if self.session:
                self.session.commit_transaction()
                logging.info("Transacción confirmada.")
        except PyMongoError as e:
            logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revertir (rollback) una transacción"""
        try:
            if self.session:
                self.session.abort_transaction()
                logging.info("Transacción revertida.")
        except PyMongoError as e:
            logging.error(f"Error al revertir la transacción: {e}")


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_documental.log"),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
    ]
)

if __name__ == "__main__":
    #Configurar el componente
    db_manager=ProductoManager(
        database_name="1dam",
        collection_name="productos"
    )
    db_manager.conectar()
    
    try:
        #db_manager.eliminar_documentos({})
        # Crear productos dentro de una transacción
        db_manager.iniciar_transaccion()
        productos=({"nombre": "Drone Phantom X", "categoria": "Drones", "precio": 1200.50, "stock": 8},
            {"nombre": "Auriculares Sonic Boom", "categoria": "Auriculares", "precio": 299.99, "stock": 15},
            {"nombre": "Cámara Action Pro", "categoria": "Cámaras", "precio": 499.99, "stock": 10},
            {"nombre": "Asistente SmartBuddy", "categoria": "Asistentes Inteligentes", "precio": 199.99,"stock": 20},
            {"nombre": "Cargador Solar Ultra", "categoria": "Accesorios", "precio": 49.99, "stock": 3})
        db_manager.insertar_productos(productos)
        db_manager.confirmar_transaccion()

        db_manager.iniciar_transaccion()
        # Consulta con proyeccion y orden
        consulta = {"categoria": "Auriculares"}
        proyeccion = {"nombre": 1, "precio": 1, "stock": 1, "_id":0}
        orden = "precio"
        db_manager.consultar_proyeccion_ordenada(consulta, proyeccion, orden)
        db_manager.confirmar_transaccion()

        db_manager.mostrar_todos_productos()

        #Actualizar documentos
        db_manager.iniciar_transaccion()
        consulta = { "$or": [{"nombre": "Drone Phantom X"}, {"nombre": "Cámara Action Pro"}] }
        db_manager.actualizar_productos(
            consulta,{"precio": 1300}
        )
        db_manager.confirmar_transaccion()
        
        db_manager.mostrar_todos_productos()

        db_manager.contar_documentos()
        # Eliminar documentos
        db_manager.iniciar_transaccion()
        db_manager.eliminar_documentos({"stock": {"$lt": 5}})
        db_manager.confirmar_transaccion()
        db_manager.contar_documentos()
        
        
        filtro= {
            "$or": [
                {"precio": {"$gt": 300}},
                {"stock": {"lt": 15}}
            ]
        }
        orden = "categoria"
        proyeccion = {"nombre": 1, "categoria": 1, "precio": 1, "_id":0}
        db_manager.consulta_compleja(filtro, proyeccion, orden)

    except Exception as e:
        logging.error(f"Error general: {e}")
        db_manager.revertir_transaccion()

    finally:
        db_manager.cerrar_conexion()


