# Dada una matriz de 4x4 con números enteros generados aleatoriamente
# entre 1 y 9, reemplaza todos los valores de la diagonal principal por el primer
# número de tu DNI 7.

import numpy as np

#Matriz aleatoria con numeros entre 1 y 9
matriz=np.random.randint(1, 10, size=(4, 4))
print(f"Matriz aleatoria: \n{matriz}")

# Cambiar los valores de la diagonal principal a 2
np.fill_diagonal(matriz, 2)
print(f"Matriz después de modificar la diagonal principal: \n{matriz}")
