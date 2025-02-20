import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

df = pd.read_csv("insurance.csv")
encoded = OrdinalEncoder()

print('Correlación de la edad con costo de seguro')
print(df[['charges','age']].corr())

print('\nCorrelación del sexo con costo de seguro')
df[['sex']] = encoded.fit_transform(df[['sex']])
df[['sex']] = df[['sex']].astype(int)
print(df[['charges', 'sex']].corr())

print('\nCorrelación del indice de peso corporal con costo de seguro')
print(df[['charges','bmi']].corr())

print('\nCorrelación del nº de hijos con costo de seguro')
print(df[['charges','children']].corr())

print('\nCorrelación de si es o no fumador con costo de seguro')
df[['smoker']] = encoded.fit_transform(df[['smoker']])
df[['smoker']] = df[['smoker']].astype(int)
print(df[['charges', 'smoker']].corr())

print('\nCorrelación de la region con costo de seguro')
df[['region']] = encoded.fit_transform(df[['region']])
df[['region']] = df[['region']].astype(int)
print(df[['charges', 'region']].corr())