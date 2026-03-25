# web-scraping-ML
# 💻 Mercado Libre Notebooks - Automated Data Pipeline
Este proyecto es un sistema "End-to-End" que monitorea precios de notebooks en Mercado Libre, almacena históricos en SQL y automatiza reportes profesionales por email.

## 🏗️ Arquitectura del Sistema
El flujo de datos está diseñado para ser completamente autónomo:
1. **Extracción (ETL):** Script en Python con `BeautifulSoup` para web scraping y `Pandas` para limpieza de datos.
2. **Almacenamiento:** Base de datos relacional `SQLite` para persistencia de datos.
3. **Automatización:** Orquestación mediante `n8n` (VPS) conectada vía **Webhooks de producción**.
4. **Programación:** Ejecución programada mediante `Task Scheduler` de Windows (Cron Job local).
5. **Notificación:** Reporte automatizado en **HTML profesional** enviado por Gmail.

## 🛠️ Tecnologías
- **Lenguaje:** Python 3.x
- **Librerías:** Requests, BeautifulSoup4, Pandas, Sqlite3.
- **Automation:** n8n, Windows Batch (.bat).

## 📊 Visualización
Los datos recolectados alimentan una app de **Streamlit** (app.py) que permite visualizar la tendencia de precios y el stock en tiempo real.
