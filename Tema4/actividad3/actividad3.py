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

#Recuperar obra de arte
obraDeArte = root.get('Gioconda')

if obraDeArte:
    print("Antes de la modificacion: ")
    print(f"Titulo: {obraDeArte.titulo}, Fecha de creacion: {obraDeArte.fechaCreacion}")
    
    #Modificar el atributo
    obraDeArte.fechaCreacion = '1605'
    transaction.commit()
    
    print("Después de la modificación:")
    print(f"Titulo: {obraDeArte.titulo}, Fecha de creacion: {obraDeArte.fechaCreacion}")
else:
    print("La obra de arte no se encontro en la base de datos")

connection.close()
db.close()