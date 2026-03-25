import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Conectamos a la base de datos que ya creaste
conexion = sqlite3.connect("hardware.db")

# 2. Leemos la tabla 'precios' directamente a un DataFrame de Pandas
df = pd.read_sql_query("SELECT * FROM precios", conexion)
conexion.close()


# 3. Obtenemos los 5 más baratos de *hoy*
# (Asumimos que la columna 'Fecha' tiene la fecha actual)
hoy = pd.Timestamp.now().strftime('%Y-%m-%d')


top5_baratos = df[df['Fecha'].str.startswith(hoy)].nsmallest(5, 'Precio')

# 4. Creamos el Gráfico
plt.figure(figsize=(10, 6)) # Tamaño de la imagen

# Barras: Nombres en el eje X, Precios en el eje Y
plt.bar(top5_baratos['NombreCorto'], top5_baratos['Precio'], color='skyblue')

# Títulos y etiquetas 
plt.title(f'Top 5 Hardware más barato del día ({hoy})', fontsize=16)
plt.xlabel('Producto (Modelo)', fontsize=12)
plt.ylabel('Precio (ARS)', fontsize=12)

# Rotamos los nombres para que se lean bien
plt.xticks(rotation=45, ha='right')

# Ajustamos el diseño para que no se corte nada
plt.tight_layout()

# 5. Guardamos el gráfico como una imagen
plt.savefig('grafico_precios_hoy.png')
print("\n✅ ¡Gráfico guardado como 'grafico_precios_hoy.png'!")

# (Opcional) Mostramos el gráfico en pantalla
plt.show()