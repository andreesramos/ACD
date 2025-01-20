import pandas as pd
from sklearn.model_selection import train_test_split

df=pd.read_csv("preciosZapatos.csv")

#Añadir columna de euros
df["price_euros"] = df["price"] * 0.0121
df=df.dropna()

print("Eliminacion de outliers")
q1 = df["price_euros"].quantile(0.25) #Primer cuartil
print("Primer cuartil: " ,q1)
q3 = df["price_euros"].quantile(0.75) #Tercer cuartil
print("Tercer cuartil: " ,q3)
iqr = q3 - q1 #Rango intercuartil

# Definir los límites inferior y superior
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print(f"Límite inferior: {lower_bound}, Límite superior: {upper_bound}")

# Filtrar valores dentro de los límites
df_sin_atipicos = df[(df["price_euros"] >= lower_bound) & (df["price_euros"] <= upper_bound)]

# Comparar el número de filas antes y después
print(f"Filas antes: {df.shape[0]}")
print(f"Filas después de eliminar atípicos: {df_sin_atipicos.shape[0]}")

print("\nNormalizacion")
# Calcular los valores mínimo y máximo de las columnas
min_price = df["price_euros"].min()
max_price = df["price_euros"].max()

print(f" Precio mínimo: {min_price}")
print(f" Precio máximo: {max_price}")

# Normalizar las columnas
df["price_euros_norm"] = (df["price_euros"] - min_price) / (max_price - min_price)

# Mostrar los resultados
print(df[["price_euros", "price_euros_norm"]].head())

print("\nDatos antes de One-Hot Encoding")
# Mostrar un ejemplo de los datos
print(df[["brand", "color"]].head())

# Aplicar One-Hot Encoding a la columna "color"
df_encoded = pd.get_dummies(df, columns=["color"], drop_first=False)

# Mostrar un ejemplo de los datos codificados
print("Datos después de aplicar One-Hot Encoding:")
print(df_encoded[["brand", "color_Red", "color_Blue", "color_Black", "color_Gold", "color_Yellow"]].head())

print("\nSeparar en columnas predictoras y objetivo")
#Variables predictoras
x = df[["brand", "color", "size"]]
#Variable objetivo
y = df["price_euros"]

print("Variables predictoras:\n" ,x.head())
print("Variable objetivo:\n" ,y.head())

print("\nSeparar los datos de entrenamiento y prueba")
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Mostrar resultados
print("Tamaño del conjunto de entrenamiento:", X_train.shape[0])
print("Tamaño del conjunto de prueba:", X_test.shape[0])

print("Conjunto de entrenamiento: \n" ,X_train.head())
print("Conjunto de prueba: \n" ,X_test.head())
print("Conjunto objetivo de entrenamiento: \n" ,y_train.head())
print("Conjunto objetivo de prueba: \n" ,y_test.head())

print("\nAplicar funciones personalizadas")
#Funcion personalizada para calcular el porcentaje de descuento
def calcular_descuento(row):
    return (row["price"] - row["offer_price"]) / row["price"] * 100

# Aplicar la función a cada fila
df["descuento(%)"] = df.apply(calcular_descuento, axis=1)
#Mostrar un ejemplo
print(df.head())