from peewee import MySQLDatabase, Model, CharField, IntegerField, PrimaryKeyField
from peewee import IntegrityError
import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent

#Funcion para saber si existe la tabla
def tabla_existe(Libros):
    consulta = "select count(*) from information_schema.tables where table_schema = %s and table_name = %s"
    cursor = db.execute_sql(consulta, ('1dam', Libros))
    resultado = cursor.fetchone()
    return resultado[0]>0

#Funcion para insertar prestamos
def insertar_prestamos():
    try:
        #Comprobar si 'prestamos' existe en root
        if 'prestamos' not in root:
            root['prestamos']={} #Si no existe crea una coleccion vacia
            transaction.commit()
        
        #Crear nuevos prestamos
        prestamo1= Prestamo(1, "Juan Perez", "2023-10-01", "2023-11-01")
        prestamo2= Prestamo(2, "Ana Lopez", "2023-09-15", "2023-10-15")
        prestamo3= Prestamo(4, "Maria Gomez", "2023-09-20", "2023-10-20")
        
        #Añadir prestamos a la colección
        root['prestamos']['1']=prestamo1
        root['prestamos']['2']=prestamo2
        root['prestamos']['4']=prestamo3
        
        #Confirmar transaccion
        transaction.commit()
        print("Préstamos almacenados correctamente en ZODB.")
    except Exception as e:
        #Revertimos la transaccion si hay error
        transaction.abort()
        print(f"Error durante la transaccion: {e}. Transaccion revertida")

#Funcion que busca los prestamos a través del género del libro
def buscar_prestamos_por_genero(generop):
    libros_genero=Libros.select().where(Libros.genero==generop)
    
    print("Prestamos de libros del género 'Novela':")
    
    #Recorre los libros que tienen de genero 'Novela'
    for libro in libros_genero:
        if libros_genero:
            disponible=False
            #Recorre los prestamos
            for clave, prestamo in root['prestamos'].items():
                #Si el prestamo contiene el campo de 'libro_id' y este es igual al id del libro, entonces imprime sus datos.
                if hasattr(prestamo, 'libro_id') and prestamo.libro_id==libro.id:
                    print(f"Libro: {libro.titulo}, Nombre usuario: {prestamo.nombre_usuario}, Fecha de prestamo: {prestamo.fecha_prestamo}, Fecha de devolucion: {prestamo.fecha_devolucion}")
                    disponible=True
            if(disponible==False):
                print("Préstamo no disponible")
        else:
            print("El género no existe")

#Conexión a la base de datos
db=MySQLDatabase(
    '1dam',
    user='usuario',
    password='usuario',
    host='localhost',
    port=3306
)

db.connect()


#Campos de la tabla Libros
class Libros(Model):
    id = PrimaryKeyField()
    titulo = CharField(100)
    autor = CharField(100)
    anio_publicacion = IntegerField()
    genero = CharField(50)
    class Meta:
        database = db
        table_name = 'Libros'
        
#Si la tabla existe la borramos
if tabla_existe(Libros._meta.table_name):
    db.drop_tables([Libros], cascade=True)
    
#Creacion de la tabla
db.create_tables([Libros])
print("Tabla 'Libros' creada con exito")

try:
    #Iniciar transaccion
    with db.atomic():
        #Insercion de datos en la tabla
        Libros.create(titulo= 'Cien años de soledad', autor= 'Gabriel García Márquez', anio_publicacion= 1967, genero= 'Novela')
        Libros.create(titulo= 'Don Quijote de la Mancha', autor= 'Miguel de Cervantes', anio_publicacion= 1605, genero= 'Novela')
        Libros.create(titulo= 'El Principito', autor= 'Antoine de Saint-Exupéry', anio_publicacion= 1943, genero= 'Infantil')
        Libros.create(titulo= 'Crónica de una muerte anunciada', autor= 'Gabriel García Márquez', anio_publicacion= 1981, genero= 'Novela')
        Libros.create(titulo= '1984', autor= 'George Orwell', anio_publicacion= 1949, genero= 'Distopía')
        print("Libros insertados correctamente en la base de datos.")
except IntegrityError as e:
    print(f"Error al insertar libros: {e}")
    
#Conexion a la base de datos
storage = ZODB.FileStorage.FileStorage('1dam.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

#Definir clase Prestamo
class Prestamo(Persistent):
    def __init__(self, libro_id, nombre_usuario, fecha_prestamo, fecha_devolucion):
        self.libro_id = libro_id
        self.nombre_usuario = nombre_usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

#Llamada a las funciones
insertar_prestamos()
buscar_prestamos_por_genero('Novela')

connection.close()
db.close()
