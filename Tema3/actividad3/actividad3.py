from peewee import MySQLDatabase, Model, CharField, IntegerField
from peewee import IntegrityError

#Definicion de la funcion para saber si existe la tabla
def tabla_existe(ObrasArte):
    consulta = "select count(*) from information_schema.tables where table_schema = %s and table_name = %s"
    cursor = db.execute_sql(consulta, ('1dam', ObrasArte))
    resultado = cursor.fetchone()
    return resultado[0]>0

#Conexion a la base de datos
db=MySQLDatabase(
    '1dam',
    user='usuario',
    password='usuario',
    host='localhost',
    port=3306
)

db.connect()
print("Conexion exitosa a la base de datos")

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
        
#Si la tabla existe se elimina
if tabla_existe(ObrasArte._meta.table_name):
    print(f"La tabla '{ObrasArte._meta.table_name}' existe.")
    db.drop_tables([ObrasArte], cascade=True)
    print(f"Tabla '{ObrasArte._meta.table_name}' eliminada con exito.")
else:
    print(f"La tabla '{ObrasArte._meta.table_name}' no existe.")

#Creacion de la tabla
db.create_tables([ObrasArte])
print("Tabla 'ObrasArte' creada con exito")


try:
    #Iniciar transacción
    with db.atomic():
        #Insercion de datos en la tabla
        ObrasArte.create(titulo='El Guernica', artista='Pablo Picasso', fechaCreacion='1937', tecnica='Oleo', museo='Reina Sofia')
        ObrasArte.create(titulo='La Capilla Sixtina', artista='Miguel Angel', fechaCreacion='1508', tecnica='Fresco comun', museo='El Vaticano')
        ObrasArte.create(titulo='La Gioconda', artista='Leonardo da Vinci', fechaCreacion='1505', tecnica='Sfumato', museo='Louvre')
        ObrasArte.create(titulo='La noche estrellada', artista='Van Gohg', fechaCreacion='1889', tecnica='Oleo', museo='MoMA')
        ObrasArte.create(titulo='las Meninas', artista='Velazquez', fechaCreacion='1656', tecnica='alla prima', museo='El Prado')
except IntegrityError as e:
    print(f"Error al insertar obras de arte: {e}")
