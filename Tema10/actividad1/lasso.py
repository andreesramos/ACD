import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error

# Cargar el dataset
df = pd.read_csv('insurance.csv', sep=',')

# Convertir variables numéricas adecuadas
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
df['charges'] = pd.to_numeric(df['charges'], errors='coerce')

# Aplicar One Hot Encoding solo a 'smoker'
df = pd.get_dummies(df, columns=['smoker'], drop_first=True)

# Seleccionar solo las variables age, bmi y smoker
columnas_predictoras = ['age', 'bmi', 'smoker_yes']
X = df[columnas_predictoras]
y = df['charges']

# Dividir en entrenamiento (80%) y test (20%)
df_train = df.sample(frac=0.8, random_state=42)
df_test = df.drop(df_train.index)

X_train = df_train[columnas_predictoras]
y_train = df_train['charges']
X_test = df_test[columnas_predictoras]
y_test = df_test['charges']

# Aplicar Regresión Lasso con un alpha (hiperparámetro de regularización)
modelo_lasso = Lasso(alpha=1.0) # Puedes ajustar alpha para cambiar la fuerza de regularización
modelo_lasso.fit(X_train, y_train)

# Predicción
y_pred = modelo_lasso.predict(X_test)

# Evaluación del error
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print(f'RMSE con Regresión Lasso: {rmse:.2f}')

# Mostrar qué variables han sido eliminadas (coeficiente = 0)
coeficientes = pd.Series(modelo_lasso.coef_, index=columnas_predictoras)
variables_seleccionadas = coeficientes[coeficientes != 0].index.tolist()
variables_eliminadas = coeficientes[coeficientes == 0].index.tolist()
print("\nVariables seleccionadas por Lasso:")
print(variables_seleccionadas)
print("\nVariables eliminadas por Lasso:")
print(variables_eliminadas)

# Seleccionar 30 personas aleatorias para la gráfica
sample_indices = np.random.choice(df_test.index, size=30, replace=False)
df_sample = df_test.loc[sample_indices].copy()
y_pred_sample = modelo_lasso.predict(df_sample[columnas_predictoras])

# Gráfica con 30 personas seleccionadas
plt.figure(figsize=(12, 6))
plt.plot(range(len(df_sample)), df_sample['charges'], marker='o', linestyle='--', color='blue', label='Datos reales', alpha=0.7)
plt.plot(range(len(df_sample)), y_pred_sample, marker='x', linestyle='--', color='red', label='Predicción', alpha=0.7)
#plt.xticks(range(len(df_sample)), labels=df_sample['age'], rotation=45)
plt.title('Regresión Lasso - Predicción de Charges (Muestra de 30 Personas)')
plt.xlabel('Persona (Individuo del dataset)')
plt.ylabel('Charges')
plt.grid(True)
plt.legend()
plt.show()