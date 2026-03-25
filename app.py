import streamlit as st
import sqlite3
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Monitor de Hardware v1.0", layout="wide")

st.title("🚀 Buscador Inteligente de Hardware")
st.markdown("Datos extraídos de Mercado Libre y almacenados en SQLite.")

# 1. Conexión a la base de datos
conn = sqlite3.connect("hardware.db")
df = pd.read_sql_query("SELECT * FROM precios", conn)
conn.close()

# 2. Filtros interactivos en la barra lateral
st.sidebar.header("Filtros")
busqueda = st.sidebar.text_input("Buscar modelo (ej: 3070, Ryzen, etc.)", "")
precio_max = st.sidebar.slider("Precio Máximo", 0, int(df['Precio'].max()), int(df['Precio'].max()))

# 3. Aplicar filtros al DataFrame
df_filtrado = df[df['Nombre'].str.contains(busqueda, case=False)]
df_filtrado = df_filtrado[df_filtrado['Precio'] <= precio_max]

# 4. Convertir el nombre en un link
if 'URL' in df_filtrado.columns:
    # Usamos 'URL' 
    df_filtrado['Producto'] = df_filtrado.apply(
        lambda x: f'<a href="{x["URL"]}" target="_blank">{x["Nombre"]}</a>', 
        axis=1
    )
else:
    st.error("No encontré la columna 'URL'. Verificá tu base de datos.")
    df_filtrado['Producto'] = df_filtrado['Nombre']

# 5. Mostrar la tabla
st.subheader("Listado de Productos")
st.write(
    df_filtrado[['Producto', 'Precio', 'Fecha']].to_html(escape=False, index=False), 
    unsafe_allow_html=True
)

# 5. Visualización
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Listado de Productos")
    # Mostramos la tabla permitiendo HTML para los links
    st.write(df_filtrado[['Producto', 'Precio', 'Fecha']].to_html(escape=False, index=False), unsafe_allow_html=True)

with col2:
    st.subheader("Distribución de Precios")
    st.bar_chart(df_filtrado.set_index('Nombre')['Precio'])

st.success(f"Se encontraron {len(df_filtrado)} productos que coinciden.")