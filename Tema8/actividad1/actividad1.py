import matplotlib.pyplot as plt;
import pandas as pd;

df = pd.read_csv('preciosZapatos.csv')

#Añadir columna de euros
df["price_euros"] = df["price"] * 0.0121
df=df.dropna()

precios_marca = df.groupby('brand')['price_euros'].mean()

#Gráfico de líneas
precios_marca.plot(title='Precios según la marca', figsize=(10, 6))
plt.show()

#Gráfico de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(df['brand'], df['price_euros'], alpha=0.6, c='blue', edgecolors='k')
plt.title("Relación entre marca y precio", fontsize=14)
plt.xlabel("Precios", fontsize=12)
plt.ylabel("Marcas", fontsize=12)
plt.xticks(rotation=90)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Gráfico de barras
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

# Histograma
df['price_euros'].plot(
   kind='hist',
   bins=20,
   title='Distribución de los precios por marca',
   figsize=(10, 6)
)
plt.show()

# Diagrama de caja
plt.boxplot(
   df['price_euros'].dropna(),
   patch_artist=True,
   boxprops=dict(facecolor="lightblue", color="blue"),
   medianprops=dict(color="red"),
   flierprops=dict(marker="o", color="darkorange", markersize=5)
)
plt.title("Diagrama de caja: Precios")
plt.xlabel("Cantidad de precios")
plt.show()