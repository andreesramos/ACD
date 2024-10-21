from peewee import MySQLDatabase, CharField, IntegerField, Model

db=MySQLDatabase(
    '1dam',
    user='usuario',
    password='usuario',
    host='localhost',
    port=3306
)

db.connect()

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

print("Tarea1...")

obras=ObrasArte.select().where(ObrasArte.fechaCreacion>1600)
for obra in obras:
    print(f"Titulo: {obra.titulo}, Artista: {obra.artista}, Museo: {obra.museo}")


print("Tarea2...")

obra=ObrasArte.get((ObrasArte.titulo == 'las Meninas') and (ObrasArte.artista == 'Velazquez'))
obra.delete_instance()
obras=ObrasArte.select()
for o in obras:
    print(f"Titulo: {o.titulo}, Artista: {o.artista}, Fecha de creacion: {o.fechaCreacion}, Tecnica: {o.tecnica}, Museo: {o.museo}")


print("Tarea3...")
ObrasArte.delete().where(ObrasArte.tecnica == 'Oleo').execute()
obras=ObrasArte.select()
for o in obras:
    print(f"Titulo: {o.titulo}, Artista: {o.artista}, Fecha de creacion: {o.fechaCreacion}, Tecnica: {o.tecnica}, Museo: {o.museo}")