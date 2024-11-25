import logging
from peewee import Model, CharField, ForeignKeyField, MySQLDatabase

# Componente DatabaseManagerORM
class DatabaseManagerORM:
    def __init__(self):
        self.db = db
        
    def conectar(self):
        """Conecta la base de datos y crea las tablas."""
        self.db.connect()
        self.db.create_tables([Proveedor, Herramienta])
        logging.info("Conexión establecida y tablas creadas.")
        
    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if not self.db.is_closed():
            self.db.close()
            logging.info("Conexión cerrada.")
            
    def iniciar_transaccion(self):
        """Inicia una transacción."""
        self.db.begin()
        logging.info("Transacción iniciada.")
        
    def confirmar_transaccion(self):
        """Confirma (commit) una transacción."""
        self.db.commit()
        logging.info("Transacción confirmada.")
        
    def revertir_transaccion(self):
        """Revierte (rollback) una transacción."""
        self.db.rollback()
        logging.info("Transacción revertida.")
        
    def crear_proveedor(self, nombre, direccion):
        """Inserta un nuevo proveedor."""
        proveedor = Proveedor.create(nombre=nombre, direccion=direccion)
        logging.info(f"Proveedor creado: {proveedor.nombre} - {proveedor.direccion}")
        return proveedor
    
    def crear_herramienta(self, nombre, tipo, marca, uso, material, proveedor_nombre):
        """Inserta una nueva herramienta."""
        try:
            proveedor = Proveedor.get(Proveedor.nombre == proveedor_nombre)
            herramienta = Herramienta.create(
                nombre=nombre,
                tipo=tipo,
                marca=marca,
                uso=uso,
                material=material,
                proveedor=proveedor
            )
            logging.info(f"Herramienta creada: {herramienta.nombre} - {herramienta.tipo}")
            return herramienta
        except Proveedor.DoesNotExist:
            logging.error(f"El proveedor '{proveedor_nombre}' no existe.")
            raise
    
    def leer_herramientas(self):
        """Lee todas las herramientas."""
        herramientas = Herramienta.select()
        logging.info("Leyendo herramientas:")
        for herramienta in herramientas:
            logging.info(f"{herramienta.nombre} - {herramienta.tipo} ({herramienta.proveedor.nombre})")  
        return herramientas
    
    def actualizar_proveedor(self, nombre, direccion):
        """Actualizar un proveedor en la base de datos"""
        proveedor = Proveedor.get(Proveedor.nombre == nombre)
        proveedor.direccion = direccion
        proveedor.save()
        return proveedor
    
    def actualizar_herramienta(self, nombre, tipo):
        """Actualizar una herramienta en la base de datos"""
        herramienta = Herramienta.get(Herramienta.nombre == nombre)
        herramienta.tipo = tipo
        herramienta.save()
        return herramienta
            
    def eliminar_herramienta(self, nombre):
        """Eliminar una herramienta de la base de datos"""
        herramienta = Herramienta.get(Herramienta.nombre == nombre)
        herramienta.delete_instance()
        return herramienta
    
    def eliminar_proveedor(self, nombre):
        """Eliminar un proveedor de la base de datos"""
        proveedor = Proveedor.get(Proveedor.nombre == nombre)
        proveedor.delete_instance()
        return proveedor

    def consultar_herramienta(self, proveedor_nombre):
        """Imprimir herramientas que pertenezcan a un proveedor"""
        try:
            proveedor = Proveedor.get(Proveedor.nombre == proveedor_nombre)
            herramientas = Herramienta.select().where(Herramienta.proveedor == proveedor)
            for herramienta in herramientas:
                logging.info(f"{herramienta.nombre} - {herramienta.tipo}")
        except Proveedor.DoesNotExist:
            logging.error(f"No existe el proveedor '{proveedor_nombre}'.")

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_orm.log"),
        logging.StreamHandler()
    ]
)

# Configuración de la base de datos MySQL
db = MySQLDatabase(
    "1dam", # Nombre de la base de datos
    user="usuario", # Usuario de MySQL
    password="usuario", # Contraseña de MySQL
    host="localhost", # Host
    port=3306 # Puerto por defecto de MySQL
)

# Modelos de la base de datos
class Proveedor(Model):
    nombre = CharField()
    direccion = CharField()
    class Meta:
        database = db
        
class Herramienta(Model):
    nombre = CharField()
    tipo = CharField()
    marca = CharField()
    uso = CharField()
    material = CharField()
    proveedor = ForeignKeyField(Proveedor, backref='herramientas')
    class Meta:
        database = db

# Flujo principal
gestion = DatabaseManagerORM()
gestion.conectar()
# Gestion de Proveedores
print("Gestión de Proveedores:")
gestion.iniciar_transaccion()
gestion.crear_proveedor("Proveedor A", "Contacto 123-456-789")
gestion.crear_proveedor("Proveedor B", "Contacto 987-654-321")
gestion.confirmar_transaccion()

# Actualización de Proveedor
print("Cambio del dato por mi DNI 12345678A al proveedor A")
gestion.iniciar_transaccion()
gestion.actualizar_proveedor("Proveedor A", "24525402L")
gestion.confirmar_transaccion()

# Eliminar Proveedor
print("Eliminar al proveedor B")
gestion.iniciar_transaccion()
gestion.eliminar_proveedor("Proveedor B")
gestion.confirmar_transaccion()

# Gestión de Herramientas
print("Gestión de Herramientas:")
gestion.iniciar_transaccion()
gestion.crear_herramienta("Martillo", "Manual", "Facom", "Percusion", "Acero", "Proveedor A")
gestion.crear_herramienta("Taladro", "Eléctrico", "Facom", "Percusion", "Acero", "Proveedor A")
gestion.confirmar_transaccion()

# Consultar herramientas
print("Herramientas asociadas al proveedor Proveedor A:")
gestion.consultar_herramienta("Proveedor A")

# Actualizar herramienta
print("Actualizar herramienta Martillo a tipo reforzado")
gestion.iniciar_transaccion()
gestion.actualizar_herramienta("Martillo", "Reforzado")
gestion.confirmar_transaccion()

# Eliminar herramienta
print("Eliminar herramienta Taladro")
gestion.iniciar_transaccion()
gestion.eliminar_herramienta("Taladro")
gestion.confirmar_transaccion()

# Desconectar
gestion.desconectar()
