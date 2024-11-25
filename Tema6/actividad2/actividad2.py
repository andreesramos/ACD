import logging
import mysql.connector
from mysql.connector import Error

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager.log"), # Logs guardados en un archivo
        logging.StreamHandler(), # Logs también en consola
    ]
)

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def conectar(self):
        """Conectar a la base de datos MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                logging.info("Conexión exitosa a la base de datos.")
        except Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            
    def desconectar(self):
        """Cerrar la conexión a la base de datos"""
        if self.connection.is_connected():
            self.connection.close()
            logging.info("Conexión cerrada.")
            
    def crear_obraArte(self, titulo, artista, fechaCreacion, tecnica, museo):
        """Insertar una nueva obra de arte en la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO ObrasArte (titulo, artista, fechaCreacion, tecnica, museo)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (titulo, artista, fechaCreacion, tecnica, museo))
            #self.connection.commit()
            logging.info(f"Obra de arte '{titulo}' insertada exitosamente.")
        except Error as e:
            logging.error(f"Error al insertar la obra de arte '{titulo}': {e}")
            
    def leer_obrasArte(self):
        """Leer todas las obras de arte de la base de datos"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM ObrasArte")
            obras = cursor.fetchall()
            logging.info("Obras de arte recuperadas:")
            for obra in obras:
                logging.info(obra)
            return obras
        except Error as e:
            logging.error(f"Error al leer las obras de arte: {e}")
            return None
        
    def actualizar_obraArte(self, titulo, artista, fechaCreacion, tecnica, museo):
        """Actualizar una obra de arte en la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE ObrasArte
                SET artista = %s, fechaCreacion = %s, tecnica = %s, museo = %s
                WHERE titulo = %s
            """
            cursor.execute(query, (artista, fechaCreacion, tecnica, museo, titulo))
            self.connection.commit()
            logging.info(f"Obra de arte con titulo{titulo} actualizada exitosamente.")
        except Error as e:
            logging.error(f"Error al actualizar la obra de arte con titulo {titulo}: {e}")
            
    def eliminar_obraArte(self, titulo):
        """Eliminar una obra de arte de la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM ObrasArte WHERE titulo = %s"
            cursor.execute(query, (titulo,))
            self.connection.commit()
            logging.info(f"Obra de arte con titulo {titulo} eliminada exitosamente.")
        except Error as e:
            logging.error(f"Error al eliminar la obra de arte con titulo {titulo}: {e}")
            
    def iniciar_transaccion(self):
        """Iniciar una transacción"""
        try:
            if self.connection.is_connected():
                self.connection.start_transaction()
                logging.info("Transacción iniciada.")
        except Error as e:
            logging.error(f"Error al iniciar la transacción: {e}")
            
    def confirmar_transaccion(self):
        """Confirmar (commit) una transacción"""
        try:
            if self.connection.is_connected():
                self.connection.commit()
                logging.info("Transacción confirmada.")
        except Error as e:
            logging.error(f"Error al confirmar la transacción: {e}")
            
    def revertir_transaccion(self):
        """Revertir (rollback) una transacción"""
        try:
            if self.connection.is_connected():
                self.connection.rollback()
                logging.info("Transacción revertida.")
        except Error as e:
            logging.error(f"Error al revertir la transacción: {e}")
            
            
if __name__ == "__main__":
    db_manager = DatabaseManager("localhost", "usuario", "usuario", "1dam")
    db_manager.conectar()
    
    # Insertar una nueva obra de arte
    db_manager.crear_obraArte("La Gioconda", "Leonardo da Vinci", 1503, "sfumato", "Louvre")
    
    # Leer todas las obras de arte
    db_manager.leer_obrasArte()
            
    # Actualizar una obra de arte
    db_manager.actualizar_obraArte("La Gioconda", "Leonardo da Vinci", 1550, "sfumato", "Louvre")
    
    # Eliminar una obra de arte
    db_manager.eliminar_obraArte("El Guernica")
    
    # Gestionar transacciones
    db_manager.iniciar_transaccion()
    db_manager.crear_obraArte("La noche estrellada", "Van Gohg", 1889, "Oleo", "MoMA")
    db_manager.revertir_transaccion() # No se guardará la inserción
    db_manager.desconectar()