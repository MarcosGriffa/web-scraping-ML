import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# 1. Tu URL 
url = "https://listado.mercadolibre.com.ar/notebook-gamer#D[A:notebook%20gamer]&origin=UNKNOWN&as.comp_t=SUG&as.comp_v=notebok&as.comp_id=SUG" 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Buscando datos...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    productos = []

    # Buscamos los contenedores de los productos 
    items = soup.select('.ui-search-result__wrapper')

    for item in items:
        # 1. Buscamos el título 
        titulo_tag = item.select_one('.ui-search-item__title') or item.select_one('.poly-component__title')
        nombre_sucio = titulo_tag.text.strip() if titulo_tag else "Producto desconocido"
        
        # 2. Buscamos el PRECIO
        precio_tag = item.select_one('.andes-money-amount__fraction')
        precio = int(precio_tag.text.replace('.', '')) if precio_tag else 0

        # 3. BUSCAMOS EL LINK 
        link_tag = item.select_one('a.ui-search-link') or item.select_one('a.poly-component__title')
        link = link_tag['href'] if link_tag else "Sin link"

        # 4. Guardamos todo en la lista
        if nombre_sucio != "Producto desconocido" and precio > 0:
            productos.append({
                "Nombre": nombre_sucio, # Acá podés aplicar tu limpieza
                "Precio": precio,
                "URL": link, # <--- ESTA ES LA NUEVA COLUMNA
                "Fecha": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
            })

    # --- PARTE DE SQL ---
    if productos:
        df = pd.DataFrame(productos)
        
        # Creamos la conexión a SQLite (se crea el archivo 'mibase.db' solo)
        conexion = sqlite3.connect("hardware.db")
        
        # Guardamos el DataFrame en una tabla llamada 'precios'
        df.to_sql("precios", conexion, if_exists="append", index=False)
        
        conexion.close()
        
        print(f"Exito! Se guardaron {len(df)} productos en 'hardware.db'")
        print(df.head(3)) # Muestra los primeros 3 para confirmar
    else:
        print("❌ No se encontraron productos.")
else:
    print(f"Error de conexión: {response.status_code}")


import requests 

# --- AVISO A n8n ---
webhook_url = "http://69.6.206.212/webhook/32dcb78b-5fca-4d65-868b-d007b648a657"


# Sacamos las 3 más baratas 
top_ofertas = df.nsmallest(3, 'Precio').to_dict(orient='records')

data_para_n8n = {
    "mensaje": "Scraping finalizado con éxito",
    "tienda": "Mercado Libre",
    "registros": len(df),
    "ofertas": top_ofertas  
}

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Enviamos los datos con los headers incluidos
response = requests.post(webhook_url, json=data_para_n8n, headers=headers)
    
if response.status_code == 200:
    print(f"Sincronizado con n8n con exito: {response.status_code}") 
else:
    print(f"Error 404: El servidor recibio la llamada pero no activo el flujo.") 