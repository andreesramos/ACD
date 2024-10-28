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

#Almacenar datos
root['Gioconda'] = ObraDeArte('La Gioconda', 'Leonardo da Vinci', 1503, 'sfumato', 'Louvre')
root['NocheEstrellada'] = ObraDeArte('La noche estrellada', 'Van Gohg', 1889, 'Oleo', 'MoMA')
root['Guernica'] = ObraDeArte('El Guernica', 'Pablo Picasso', 1937, 'Oleo', 'Reina Sofia')

transaction.commit()

tecnica_deseada="Oleo"

#Imprimir obras de arte filtradas por tecnica
for clave, obraDeArte in root.items():
    if hasattr(obraDeArte, 'tecnica') and obraDeArte.tecnica == tecnica_deseada:
        print(f"Titulo: {obraDeArte.titulo}, Artista: {obraDeArte.artista}, Fecha de creacion: {obraDeArte.fechaCreacion}, Tecnica: {obraDeArte.tecnica}, Museo: {obraDeArte.museo}")

connection.close()
db.close()
