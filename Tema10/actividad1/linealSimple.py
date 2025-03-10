import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Cargar el dataset
file_path = "insurance.csv"
df = pd.read_csv(file_path, sep=',')

# Convertir Age a numérico
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df = df.dropna(subset=['age'])

# Seleccionar columnas necesarias
df = df[['age', 'charges']]

# Dividir en entrenamiento y test (80% entrenamiento, 20% test)
df_train = df.sample(frac=0.8, random_state=42)
df_test = df.drop(df_train.index)

# Variables predictoras y objetivo
X_train = df_train[['age']]
y_train = df_train['charges']
X_test = df_test[['age']]
y_test = df_test['charges']

# Modelo de regresión lineal simple
modelo_lineal = LinearRegression()
modelo_lineal.fit(X_train, y_train)

# Predicción
y_pred = modelo_lineal.predict(X_test)

# Evaluación del error
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print(f'RMSE con Regresión Lineal Simple (Predictor: Age): {rmse:.2f}')

# Seleccionar 30 personas aleatorias del conjunto de prueba para visualización
sample_indices = np.random.choice(df_test.index, size=30, replace=False)
df_sample = df_test.loc[sample_indices].copy()
y_pred_sample = modelo_lineal.predict(df_sample[['age']])

# Crear gráfico con 30 personas seleccionadas
plt.figure(figsize=(12, 6))
plt.plot(range(len(df_sample)), df_sample['charges'], marker='o', color='blue', linestyle='--', label='Datos reales')
plt.plot(range(len(df_sample)), y_pred_sample, marker='x', color='red', linestyle='--', label='Predicción')
#plt.xticks(range(len(df_sample)), labels=df_sample['age'], rotation=45)
plt.title('Regresión Lineal Simple - Predictor: Age (Muestra de 30 Personas)')
plt.xlabel('Persona (Individuo del dataset)')
plt.ylabel('Charges')
plt.grid(True)
plt.legend()
plt.show()
