import ZODB, ZODB.FileStorage, transaction

#Conexión a la base de datos
storage = ZODB.FileStorage.FileStorage('1dam.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

#Almacenar lista simple en la base de datos
root['obras_arte'] = ['Gioconda', 'Meninas', 'Guernica']
transaction.commit() #Confirmar cambios

#Mostrar lista almacenada
print(root['obras_arte'])

#Cerrar conexión y base de datos
connection.close()
db.close()