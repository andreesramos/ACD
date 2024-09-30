import random; #Importo la librería random para poder generar numeros aleatorios

lista=[]; #Creo una lista vacia para poder añadir elementos

for i in range(1, 11):
    lista.append(random.randint(1,50));
    #Uso la función randint de random para añadir números aleatorios(entre 1 y 50)
    #a la lista

print(lista);

num = int(input("Introduce un numero: "));

if num in lista:
    print("¡Bingo!");
else:
    print("No esta");
