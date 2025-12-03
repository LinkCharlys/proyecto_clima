# main_etl.py
import subprocess
import os
import sqlite3
from etl.extract import fetch_weather_data
from etl.transform import transform_data
from etl.load import load_data, DATABASE_FILE

def setup_database():
    """Crea la BD y las tablas leyendo schema.sql."""
    print("--- 1. CONFIGURACIÓN DE BASE DE DATOS ---")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        with open('schema.sql', 'r') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.close()
        print(f"Base de datos {DATABASE_FILE} y tablas creadas/verificadas.")
    except Exception as e:
        print(f"ERROR: Fallo al configurar la BD. Detalle: {e}")
        exit()

def run_etl_pipeline():
    """Ejecuta el proceso completo ETL de inicio a fin (Instrucción 8)."""
    print("\n--- 2. INICIO DEL PROCESO ETL COMPLETO ---")
    
    # E: Extracción
    print("-> 2.1 EXTRAYENDO datos de la API...")
    raw_data = fetch_weather_data()
    
    # T: Transformación
    print("-> 2.2 TRANSFORMANDO y estructurando los datos...")
    df_ciudades, df_pronostico = transform_data(raw_data)

    # L: Carga
    print("-> 2.3 CARGANDO datos a la base de datos SQL...")
    load_data(df_ciudades, df_pronostico)
    print("-> PROCESO ETL COMPLETADO SATISFACTORIAMENTE.")

if __name__ == "__main__":
    setup_database()
    run_etl_pipeline()