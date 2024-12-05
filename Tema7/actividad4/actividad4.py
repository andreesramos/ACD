# Usa linspace para generar un array de 50 valores igualmente distribuidos
# entre -1 y 1. Calcula el seno de cada valor y muestra ambos arrays.

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1, 1, 50)
y = np.sin(x)

print(f"Matriz de valores entre -1 y 1: \n{x}")
print(f"Matriz del seno de la amtriz x: \n{y}")
