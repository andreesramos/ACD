from persistent import Persistent
import transaction, ZODB, ZODB.FileStorage, copy

#Definimos las clases
class ObraDeArte(Persistent):
    def __init__(self, titulo, artista, fechaCreacion, tecnica, museo, id_premio):
        self.titulo = titulo
        self.artista = artista
        self.fechaCreacion = fechaCreacion
        self.tecnica = tecnica
        self.museo = museo
        self.id_premio = id_premio

class Premio(Persistent):
    def __init__(self, id, nombre_premio, fecha):
        self.id = id
        self.nombre_premio = nombre_premio
        self.fecha = fecha

#Conexión a la base de datos
storage = ZODB.FileStorage.FileStorage('1dam.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

#Verificar y crear colecciones si no existen
if 'obrasDeArte' not in root:
    root['obrasDeArte'] = {}
    
if 'premios' not in root:
    root['premios'] = {}
    
#Insertar datos en Premio
root['premios']['Premio1'] = Premio(1, "Premio1", 1972)
root['premios']['Premio2'] = Premio(2, "Premio2", 1954)

#Añadir obras de arte a la coleccion
root['obrasDeArte']["Las Meninas"]=ObraDeArte("Las Meninas", "Velazquez", 1656, "alla prima", "El Prado", 1)
root['obrasDeArte']["La Capilla Sixtina"]=ObraDeArte("La Capilla Sixtina", "Miguel Angel", 1508, "fresco comun", "El Vaticano", 2)
root['obrasDeArte']["La Ultima Cena"]=ObraDeArte("La Ultima Cena", "Leonardo da Vinci", 1498, "Oleo", "Santa Maria de las Gracias", 1)

transaction.commit()

obraDeArte_original = root['obrasDeArte']["Las Meninas"]
obraDeArte_copia = copy.deepcopy(obraDeArte_original)

obraDeArte_copia.fechaCreacion = 1700
print(f"Obra de arte original:\n Fecha de creacion: {obraDeArte_original.fechaCreacion}")
print(f"Copia de la Obra de Arte:\n Fecha de creacion: {obraDeArte_copia.fechaCreacion}")


connection.close()
db.close()