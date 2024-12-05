# Crea un array de 10 elementos con valores entre 0 y 100. Filtra y muestra
# solo los valores que sean mayores a 50.

import numpy as np

#Crear un array de 10 elementos con valores entre 0 y 100
array = np.random.randint(1, 100, size=(1, 10))
print(f"Array de 10 elementos: \n{array}")

# Filtrar y mostrar solo los valores mayores a 50
arrayFiltrado = array[array>50]
print(f"Valores mayores a 50: \n{arrayFiltrado}")