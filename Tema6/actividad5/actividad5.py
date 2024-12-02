import logging
import transaction
from ZODB import DB, FileStorage
from persistent import Persistent

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_object.log"),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
    ]
)

class ObraArte(Persistent):
    """Clase que representa una obra de arte."""
    def __init__(self, titulo, artista, fechaCreacion, tecnica, museo):
        self.titulo = titulo
        self.artista = artista
        self.fechaCreacion = fechaCreacion
        self.tecnica = tecnica
        self.museo = museo

class DatabaseManagerObject:
    """Componente para gestionar bases de datos orientadas a objetos con ZODB."""
    def __init__(self, filepath="1dam.fs"):
        self.filepath = filepath
        self.db = None
        self.connection = None
        self.root = None
        self.transaccion_iniciada = False

    def conectar(self):
        """Conecta a la base de datos ZODB."""
        try:
            storage = FileStorage.FileStorage(self.filepath)
            self.db = DB(storage)
            self.connection = self.db.open()
            self.root = self.connection.root()
            if "obrasArte" not in self.root:
                self.root["obrasArte"] = {}
                transaction.commit()
            logging.info("Conexión establecida con ZODB.")
        except Exception as e:
            logging.error(f"Error al conectar a ZODB: {e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        try:
            if self.connection:
                self.connection.close()
                self.db.close()
            logging.info("Conexión a ZODB cerrada.")
        except Exception as e:
            logging.error(f"Error al cerrar la conexión a ZODB: {e}")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        try:
            transaction.begin()
            self.transaccion_iniciada = True
            logging.info("Transacción iniciada.")
        except Exception as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirma la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.commit()
                self.transaccion_iniciada = False
                logging.info("Transacción confirmada.")
            except Exception as e:
                logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revierte la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.abort()
                self.transaccion_iniciada = False
                logging.info("Transacción revertida.")
            except Exception as e:
                logging.error(f"Error al revertir la transacción: {e}")

    def crear_obraArte(self, id, titulo, artista, fechaCreacion, tecnica, museo):
        """Crea y almacena una nueva obra de arte."""
        try:
            if id in self.root["obrasArte"]:
                raise ValueError(f"Ya existe una obra de arte con ID {id}.")
            self.root["obrasArte"][id] = ObraArte(titulo, artista, fechaCreacion, tecnica, museo)
            logging.info(f"Obra de arte con ID {id} creada exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear la obra de arte con ID {id}: {e}")

    def leer_obrasArte(self):
        """Lee y muestra todas las obras de arte almacenadas."""
        try:
            obras = self.root["obrasArte"]
            for id, obra in obras.items():
                logging.info(
                    f"ID: {id}, Titulo: {obra.titulo}, Artista: {obra.artista}, "
                    f"Fecha de creacion: {obra.fechaCreacion}, Tecnica: {obra.tecnica}, Museo: {obra.museo}"
                )
            return obras
        except Exception as e:
            logging.error(f"Error al leer las obras de arte: {e}")

    def actualizar_obrasArte(self, id, titulo, artista, fechaCreacion, tecnica, museo):
        """Actualiza los atributos de una obra de arte."""
        try:
            obra = self.root["obrasArte"].get(id)
            if not obra:
                raise ValueError(f"No existe una obra de arte con ID {id}.")
            obra.titulo = titulo
            obra.artista = artista
            obra.fechaCreacion = fechaCreacion
            obra.tecnica = tecnica
            obra.museo = museo
            logging.info(f"Obra de arte con ID {id} actualizada exitosamente.")
        except Exception as e:
            logging.error(f"Error al actualizar la obra de arte con ID {id}: {e}")

    def eliminar_obraArte(self, id):
        """Elimina una obra de arte por su ID."""
        try:
            if id not in self.root["obrasArte"]:
                raise ValueError(f"No existe una obra de arte con ID {id}.")
            del self.root["obrasArte"][id]
            logging.info(f"Obra de arte con ID {id} eliminada exitosamente.")
        except Exception as e:
            logging.error(f"Error al eliminar la obra ed arte con ID {id}: {e}")


if __name__ == "__main__":
    manager = DatabaseManagerObject()
    manager.conectar()

    # Crear obras de arte con transacción
    manager.iniciar_transaccion()
    manager.crear_obraArte(1, "La Gioconda", "Leonardo da Vinci", "1503", "sfumato", "Louvre")
    manager.crear_obraArte(2, "Las Meninas", "Velazquez", "1656", "alla prima", "El Prado")
    manager.crear_obraArte(3, "El Guernica", "Pablo Picasso", "1937", "oleo", "Reina Sofia")
    manager.confirmar_transaccion()

    # Leer obras de arte
    manager.leer_obrasArte()

    #Insertar obre de arte con id que ya existe para revertir la transaccion
    manager.iniciar_transaccion()
    try:
        manager.crear_obraArte(2, "La noche estrellada", "Van Gohg", "1889", "oleo", "MoMA")
        manager.confirmar_transaccion()
    except ValueError as e:
        manager.revertir_transaccion()

    #Mostrar obras de arte
    manager.leer_obrasArte()

    # Actualizar una obra de arte con transacción
    manager.iniciar_transaccion()
    manager.actualizar_obrasArte(1, "La Gioconda", "Leonardo da Vinci", "1600", "oleo", "Louvre")
    manager.confirmar_transaccion()

    #Mostrar obras de arte
    manager.leer_obrasArte()

    # Eliminar una obra de arte con transacción
    manager.iniciar_transaccion()
    try:
        manager.eliminar_obraArte(5)
        manager.confirmar_transaccion()
    except ValueError as e:
        manager.revertir_transaccion()

    # Leer obras de arte nuevamente
    manager.leer_obrasArte()
