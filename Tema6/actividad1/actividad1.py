import json
import csv
import logging
import os
from datetime import datetime
from copy import deepcopy

class DataManager:
    def __init__(self, ruta_archivo, tipo_archivo='json'):
        self.ruta_archivo = ruta_archivo
        self.tipo_archivo = tipo_archivo
        self.version = 1
        self.transaccion_activa = False
        self.copia_datos = None
        # Cargar datos si el archivo existe, o inicializar con un diccionario vacío
        if os.path.exists(ruta_archivo):
            self.datos = self._leer_archivo()
            logging.info(f"Archivo {tipo_archivo.upper()} cargado con éxito. Versión actual: {self.version}")
        else:
            self.datos = []
            self._guardar_archivo()
            
    def _leer_archivo(self):
        if self.tipo_archivo == 'json':
            with open(self.ruta_archivo, 'r') as archivo:
                return json.load(archivo)
        elif self.tipo_archivo == 'csv':
            datos = []
            with open(self.ruta_archivo, mode='r') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    datos.append(fila)
            return datos
        else:
            raise ValueError("Tipo de archivo no soportado. Use 'json' o 'csv'.")

    def _guardar_archivo(self):
        if self.tipo_archivo == 'json':
            with open(self.ruta_archivo, 'w') as archivo:
                json.dump(self.datos, archivo, indent=4)
        elif self.tipo_archivo == 'csv':
            if self.datos:
                with open(self.ruta_archivo, mode='w', newline='') as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=self.datos[0].keys())
                    escritor.writeheader()
                    escritor.writerows(self.datos)
                    logging.info(f"Archivo {self.tipo_archivo.upper()} guardado. Versión actual: {self.version}")
                    
    def iniciar_transaccion(self):
        if self.transaccion_activa:
            raise Exception("Ya hay una transacción activa.")
        self.transaccion_activa = True
        self.copia_datos = deepcopy(self.datos) # Crear una copia de seguridad de los datos
        logging.info("Transacción iniciada.")
        
    def confirmar_transaccion(self):
        if not self.transaccion_activa:
            raise Exception("No hay una transacción activa para confirmar.")
        self.version += 1 # Incrementa la versión al confirmar la transacción
        self.transaccion_activa = False
        self.copia_datos = None # Limpiar la copia de seguridad
        self._guardar_archivo() # Guardar cambios en el archivo
        logging.info("Transacción confirmada y cambios guardados.")
        
    def revertir_transaccion(self):
        if not self.transaccion_activa:
            raise Exception("No hay una transacción activa para revertir.")
        self.datos = self.copia_datos # Revertir a la copia de seguridad
        self.transaccion_activa = False
        self.copia_datos = None
        logging.warning("Transacción revertida. Los cambios no se guardaron.")
            
    def leer_dato(self, clave, valor):
        return [dato for dato in self.datos if dato.get(clave) == valor]
    
    def escribir_dato(self, nuevo_dato):
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de realizar cambios.")
        self.datos.append(nuevo_dato)
        logging.info(f"Dato agregado: {nuevo_dato}")
        
    def eliminar_dato(self, clave, valor):
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de realizar cambios.")
        self.datos = [dato for dato in self.datos if dato.get(clave) != valor]
        logging.info(f"Datos con {clave}={valor} eliminados.")
        
    def obtener_configuracion(self):
        return {
            "ruta_archivo": self.ruta_archivo,
            "tipo_archivo": self.tipo_archivo,
            "version": self.version,
            "transaccion_activa": self.transaccion_activa
        }
        
    def actualizar_configuracion(self, nueva_ruta, nuevo_tipo=None):
        if self.transaccion_activa:
            raise Exception("No se puede cambiar la configuración durante una transacción.")
        self.ruta_archivo = nueva_ruta
        if nuevo_tipo:
            self.tipo_archivo = nuevo_tipo
            logging.info(f"Configuración actualizada. Nueva ruta del archivo: {self.ruta_archivo}")


# Configuración de logging para guardar en un archivo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log_datos.log"), # Guardar logs en un archivo
    ]
)

#Datos
obras=[
    {"titulo": "La noche estrellada", "artista": "Van Gogh", "fechaCreacion": 1889, "tecnica": "Oleo", "museo": "MoMA"},
    {"titulo": "La Gioconda", "artista": "Leonardo da Vinci", "fechaCreacion": 1503, "tecnica": "sfumato", "museo": "Louvre"},
    {"titulo": "Las meninas", "artista": "Velazquez", "fechaCreacion": 1656, "tecnica": "alla prima", "museo": "El Prado"}
]

#Crea archivo json
gestor = DataManager("obras.json", tipo_archivo="json")

#Inicia transaccion, escribe los datos y confirma
gestor.iniciar_transaccion()
for obra in obras:
    gestor.escribir_dato(obra)
gestor.confirmar_transaccion()

#Cambiar configuracion para csv
gestor.actualizar_configuracion("obras.csv", nuevo_tipo="csv")

#Inicia transaccion y confirma
gestor.iniciar_transaccion()
gestor.confirmar_transaccion()