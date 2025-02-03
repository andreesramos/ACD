import matplotlib.pyplot as plt;
import pandas as pd;

df = pd.read_csv('preciosZapatos.csv')

#Añadir columna de euros
df["price_euros"] = df["price"] * 0.0121
df=df.dropna()

precios_marca = df.groupby('brand')['price_euros'].mean()

#Crear gráfico de líneas
precios_marca.plot(title='Precios según la marca', figsize=(10, 6))
plt.show()

#Crear gráfico de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(df['brand'], df['price_euros'], alpha=0.6, c='blue', edgecolors='k')
plt.title("Relación entre marca y precio", fontsize=14)
plt.xlabel("Precios", fontsize=12)
plt.ylabel("Marcas", fontsize=12)
plt.xticks(rotation=90)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Crear gráfico de barras
talla_especifica = '7'
df_talla = df[df['size'] == talla_especifica]
df_talla = df_talla.groupby('brand')['price_euros'].mean().reset_index()

df_talla.plot(
 kind='bar',
 x='brand',
 y='price_euros',
 title=f'Precio por marca para la talla {talla_especifica}',
 figsize=(10, 8)
)
plt.show()