from peewee import MySQLDatabase, CharField, IntegerField, Model

#Conexión a la base de datos
db=MySQLDatabase(
    '1dam',
    user='usuario',
    password='usuario',
    host='localhost',
    port=3306
)

db.connect()

#Columnas de la tabla
class ObrasArte(Model):
    titulo = CharField()
    artista = CharField()
    fechaCreacion = CharField()
    tecnica = CharField()
    museo = CharField()
    museo_id = IntegerField()
    class Meta:
        database = db
        table_name = 'ObrasArte'

#Mostramos registros iniciales
print("Registros iniciales: ")
obras=ObrasArte.select()
for o in obras:
    print(f"Titulo: {o.titulo}, Artista: {o.artista}, Fecha de creacion: {o.fechaCreacion}, Tecnica: {o.tecnica}, Museo: {o.museo}")


print("\nTarea1...")
#Mostramos las obras creadas a partir de 1600
obras=ObrasArte.select().where(ObrasArte.fechaCreacion>1600)
for obra in obras:
    print(f"Titulo: {obra.titulo}, Artista: {obra.artista}, Museo: {obra.museo}")


print("\nTarea2...")
print("Antes de la eliminacion: ")
obras=ObrasArte.select()
for o in obras:
    print(f"Titulo: {o.titulo}, Artista: {o.artista}, Fecha de creacion: {o.fechaCreacion}, Tecnica: {o.tecnica}, Museo: {o.museo}")

#Mostramos las obras al eliminar las que contienen los siguientes nombres
print("\nTras eliminar: ")
obra=ObrasArte.get((ObrasArte.titulo == 'las Meninas') & (ObrasArte.artista == 'Velazquez'))
obra.delete_instance()
obras=ObrasArte.select()
for o in obras:
    print(f"Titulo: {o.titulo}, Artista: {o.artista}, Fecha de creacion: {o.fechaCreacion}, Tecnica: {o.tecnica}, Museo: {o.museo}")


print("\nTarea3...")
print("Antes de la eliminacion: ")
obras=ObrasArte.select()
for o in obras:
    print(f"Titulo: {o.titulo}, Artista: {o.artista}, Fecha de creacion: {o.fechaCreacion}, Tecnica: {o.tecnica}, Museo: {o.museo}")

#Mostramos las obras al eliminar las creadas con la técnica de Óleo
print("\nTras eliminar: ")
ObrasArte.delete().where(ObrasArte.tecnica == 'Oleo').execute()
obras=ObrasArte.select()
for o in obras:
    print(f"Titulo: {o.titulo}, Artista: {o.artista}, Fecha de creacion: {o.fechaCreacion}, Tecnica: {o.tecnica}, Museo: {o.museo}")