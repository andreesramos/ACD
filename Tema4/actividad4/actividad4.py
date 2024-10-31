import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent

#Definir clase ObraDeArte
class ObraDeArte(Persistent):
    def __init__(self, titulo, artista, fechaCreacion, tecnica, museo):
        self.titulo = titulo
        self.artista = artista
        self.fechaCreacion = fechaCreacion
        self.tecnica = tecnica
        self.museo = museo

#Conexion a la base de datos
storage = ZODB.FileStorage.FileStorage('1dam.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

def insertar_obrasDeArte():
    try:
        print("Iniciando la transacción para agregar obras de arte...")
        
        #Comprobar si 'obrasDeArte existe en root
        if 'obrasDeArte' not in root:
            root['obrasDeArte']={} #Si no existe crea una coleccion vacia
            transaction.commit()
            
        #Crear nuevas obras de arte
        obra1= ObraDeArte("Las Meninas", "Velazquez", 1656, "alla prima", "El Prado")
        obra2= ObraDeArte("La Capilla Sixtina", "Miguel Angel", 1508, "fresco comun", "El Vaticano")
        obra3= ObraDeArte("La Ultima Cena", "Leonardo da Vinci", 1498, "Oleo", "Santa Maria de las Gracias")
        
        #Añadir obras de arte a la coleccion
        root['obrasDeArte']["Las Meninas"]=obra1
        root['obrasDeArte']["La Capilla Sixtina"]=obra2
        root['obrasDeArte']["La Ultima Cena"]=obra3
        
        transaction.commit()
        print("Transacción completada: Obras de arte añadidas correctamente.")
        for clave, obraDeArte in root['obrasDeArte'].items():
            print(f"Titulo: {obraDeArte.titulo}, Artista: {obraDeArte.artista}, Fecha de creacion: {obraDeArte.fechaCreacion}, Tecnica: {obraDeArte.tecnica}, Museo: {obraDeArte.museo}")
    except Exception as e:
        #Revertimos la transaccion si hay error
        transaction.abort()
        print(f"Error durante la transaccion: {e}. Transaccion revertida")

#Llamada a la funcion
insertar_obrasDeArte()
connection.close()
db.close()