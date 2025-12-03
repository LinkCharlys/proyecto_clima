# etl/load.py
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError # Importamos el error específico

DATABASE_FILE = 'clima_db.sqlite'
ENGINE = create_engine(f'sqlite:///{DATABASE_FILE}')

def load_data(df_ciudades, df_pronostico):
    
    # --- Carga de DIM_CIUDADES ---
    print("Cargando DIM_CIUDADES...")
    try:
        # Intentamos cargar las ciudades. Si ya existen, la BD lanza IntegrityError
        df_ciudades.to_sql('DIM_CIUDADES', ENGINE, if_exists='append', index=False)
        print("  -> Nuevas ciudades insertadas exitosamente.")
    except IntegrityError:
        # Si falla por clave duplicada (IntegrityError), lo ignoramos y seguimos.
        print("  -> Las ciudades ya existen en la BD. Saltando inserción de DIM_CIUDADES.")
    except Exception as e:
        print(f"Error inesperado al cargar DIM_CIUDADES: {e}")

    # --- Carga de FACT_PRONOSTICO (siempre se acumula) ---
    print("Cargando FACT_PRONOSTICO...")
    df_pronostico.to_sql('FACT_PRONOSTICO', ENGINE, if_exists='append', index=False)
    print("Carga completada sin errores.")