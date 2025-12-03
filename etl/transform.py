# etl/transform.py
import pandas as pd

def transform_data(raw_data):
    """
    Limpia y organiza los datos en DataFrames de Pandas.
    """
    ciudades_list = []
    pronostico_list = []
    
    for record in raw_data:
        loc = record.get('location', {})
        current = record.get('current', {})

        # DIM_CIUDADES
        ciudad_data = {
            'nombre': loc.get('name'),
            'pais': loc.get('country'),
            'latitud': loc.get('lat'),
            'longitud': loc.get('lon')
        }
        ciudades_list.append(ciudad_data)

        # FACT_PRONOSTICO
        pronostico_data = {
            'nombre_ciudad': loc.get('name'),
            'timestamp_registro': current.get('last_updated'),
            'temperatura_c': current.get('temp_c'),
            'temperatura_min_c': current.get('feelslike_c'), # Usamos feelslike
            'temperatura_max_c': current.get('temp_c'), 
            'humedad': current.get('humidity'),
            'presion': current.get('pressure_mb'),
            'descripcion_clima': current.get('condition', {}).get('text')
        }
        pronostico_list.append(pronostico_data)

    # Procesamiento de DataFrames y creación de la Clave Foránea (FK)
    df_ciudades = pd.DataFrame(ciudades_list).drop_duplicates(subset=['nombre', 'pais']).reset_index(drop=True)
    df_ciudades['id_ciudad'] = df_ciudades.index + 1 
    df_ciudades_final = df_ciudades[['id_ciudad', 'nombre', 'pais', 'latitud', 'longitud']]

    df_pronostico = pd.DataFrame(pronostico_list)
    df_pronostico = pd.merge(
        df_pronostico, 
        df_ciudades[['nombre', 'id_ciudad']], 
        left_on='nombre_ciudad', 
        right_on='nombre',
        how='left'
    )
    
    df_pronostico.rename(columns={'id_ciudad': 'ciudad_id'}, inplace=True)
    df_pronostico['timestamp_registro'] = pd.to_datetime(df_pronostico['timestamp_registro']).dt.strftime('%Y-%m-%d %H:%M:%S')

    df_pronostico_final = df_pronostico[[
        'ciudad_id', 'timestamp_registro', 'temperatura_c', 
        'temperatura_min_c', 'temperatura_max_c', 'humedad', 
        'presion', 'descripcion_clima'
    ]].dropna(subset=['ciudad_id'])

    return df_ciudades_final, df_pronostico_final