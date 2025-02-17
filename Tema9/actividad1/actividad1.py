import pandas as pd;

df = pd.read_csv('preciosZapatos.csv')

#Añadir columna de euros
df["price_euros"] = df["price"] * 0.0121

#One-Hot Encoding
df_encoded_color = pd.get_dummies(df, columns=["color"], drop_first=False)
df_encoded_brand = pd.get_dummies(df, columns=["brand"], drop_first=False)

print(df_encoded_color.head())

# print(df[['brand', 'price_euros']].corr())
# print(df[['size', 'price_euros']].corr())
# print(df[['color', 'price_euros']].corr())