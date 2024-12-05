# Dado un array de 20 elementos con valores aleatorios entre 0 y 50,
# reestructura el array en una matriz de 4x5. Luego, calcula la suma de cada
# columna.

import numpy as np

#Array aleatorio entre 0 y 50
array = np.random.randint(0, 50, size=(1, 20))
print(f"Array aleatorio: \n{array}")

#Reestructurar en 4 filas y 5 columnas
array_nuevo = array.reshape((4, 5))
print(f"Array reestructurado: \n{array_nuevo}")

#Suma de cada columna
print(f"Suma por columnas: \n{array_nuevo.sum(axis=0)}")