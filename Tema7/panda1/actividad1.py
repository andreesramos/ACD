import pandas as pd

df = pd.read_csv("preciosZapatos.csv")

print(df.shape)
print(df.shape[0])
print(df.shape[1])

print("\nHead")
print(df.head())

print("\nInfo")
print(df.info())

print("\nDescribe")
print(df.describe())

print("\nColumnas mas importantes: ")
zapatos = df[["brand", "size", "price", "offer_price"]]
print(zapatos.head())

print("\nAgregar columna:")
df["price_euros"] = df["price"] * 0.0121
print(df.head())

print("\nFiltrar filas por condicion")
mas_de_50 = df[df["price_euros"] > 50]
print(mas_de_50.head())

print("\nEliminar fila con valores nulos")
df_limpio = df.dropna()
print(f"Filas antes: {df.shape[0]}")
print(f"Filas después: {df_limpio.shape[0]}")

print("\nRellenar valores nulos")
print("\nAntes")
print(df.head(6))
df["price"]= df["price"].fillna(1935287)
df["offer_price"] = df["offer_price"].fillna(1074516)
df["price_euros"] = df["price_euros"].fillna(df["price"]*0.0121)
print("\nDespues")
print(df.head(6))

print("\nAgrupar por tallas: ")
conteo_por_tallas = df.groupby("size").size()
print(conteo_por_tallas)
promedio_precio_euros = df.groupby("size")[["price_euros"]].mean()
print("\nPromedio de precio en euros por talla: ")
print(promedio_precio_euros)