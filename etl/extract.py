# etl/extract.py
import requests
import toml # Importamos la librería para leer TOML

# --- LEER CONFIGURACIÓN ---
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    print("Error: El archivo config.toml no fue encontrado.")
    exit()

API_KEY = config['api']['key']
BASE_URL = config['api']['base_url']
CIUDADES = config['ciudades']['lista']
# -------------------------

def fetch_weather_data():
    """
    Obtiene la información de clima actual de la API.
    """
    all_data = []
    
    for city in CIUDADES:
        params = {
            "key": API_KEY,
            "q": city,
            "aqi": "no"
        }
        
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status() 
            data = response.json()      
            all_data.append(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de {city}: {e}")
            
    return all_data