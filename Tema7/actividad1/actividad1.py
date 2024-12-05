#Crea una matriz de ceros de tamaño 3x4. Cambia los valores de la primera
#fila a unos y los de la última fila a la última cifra de tu DNI.

import numpy as np

#Matriz de ceros
matriz = np.zeros((3, 4))
print(f"Matriz de ceros: \n{matriz}")

#Modificar primera y ultima fila
matriz[0:1, 0:4]=1
matriz[2:3, 0:4]=4
print(f"Matriz modificada: \n{matriz}")
