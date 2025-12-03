import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="Análisis del Clima Global",
    page_icon="🌍"
)
# CONEXIÓN A LA BASE DE DATOS SQL (Instrucción 10)
DATABASE_FILE = 'clima_db.sqlite' 
# Usamos check_same_thread=False para evitar problemas de concurrencia de SQLite en la web.
CONN = sqlite3.connect(DATABASE_FILE, check_same_thread=False)

@st.cache_data
def load_data_from_db():
    """
    Función que lee los datos unidos de DIM_CIUDADES y FACT_PRONOSTICO.
    """
    query = """
    SELECT 
        T1.nombre AS ciudad_nombre,
        T2.timestamp_registro,
        T2.temperatura_c,
        T2.humedad,
        T2.presion
    FROM DIM_CIUDADES T1
    JOIN FACT_PRONOSTICO T2 ON T1.id_ciudad = T2.ciudad_id
    ORDER BY T2.timestamp_registro DESC;
    """
    df = pd.read_sql_query(query, CONN)
    df['timestamp_registro'] = pd.to_datetime(df['timestamp_registro'])
    return df

# --- INTERFAZ DE STREAMLIT ---
df_full = load_data_from_db()

st.title("🌎 Análisis del Clima Urbano")
st.markdown("Dashboard interactivo que muestra los datos cargados en SQLite.")

if df_full.empty:
    st.warning("No hay datos disponibles. Por favor, ejecuta 'python main_etl.py' y verifica que el archivo 'clima_db.sqlite' se haya creado.")
    st.stop()
    
# --- FILTROS/CONTROLES (Requisito 2 Filtros - Instrucción 12) ---
st.sidebar.header("Filtros")

# 1. Filtro de Categoría (Selector de Ciudad)
available_cities = df_full['ciudad_nombre'].unique()
selected_cities = st.sidebar.multiselect(
    "1. Selecciona las Ciudades",
    options=available_cities,
    default=available_cities
)

# 2. Filtro de Rango Numérico (Slider de Humedad)
min_hum = df_full['humedad'].min()
max_hum = df_full['humedad'].max()
humedad_range = st.sidebar.slider(
    "2. Rango de Humedad (%)",
    min_value=int(min_hum),
    max_value=int(max_hum),
    value=(int(min_hum), int(max_hum))
)

# 3. Filtro de Rango Numérico (Slider de Presión)
min_pres = df_full['presion'].min()
max_pres = df_full['presion'].max()
presion_range = st.sidebar.slider(
    "3. Rango de Presión (hPa)",
    min_value=int(min_pres),
    max_value=int(max_pres),
    value=(int(min_pres), int(max_pres))
)

# 4. Filtro de Rango Temporal (Horas hacia atrás)
max_hours_back = 48 
hours_back = st.sidebar.slider(
    "4. Historial (Horas atrás)",
    min_value=1,
    max_value=max_hours_back,
    value=48, # <--- MODIFICADO A 48 HORAS POR DEFECTO
    step=1
)

# --- CALCULAR HORA DE CORTE (DEFINICIÓN CORRECTA) ---
# Esta sección debe ir después de definir 'hours_back' y antes de usar 'cutoff_time'
latest_timestamp = df_full['timestamp_registro'].max()
cutoff_time = latest_timestamp - pd.Timedelta(hours=hours_back)


# Aplicar los 4 filtros
df_filtered = df_full[df_full['ciudad_nombre'].isin(selected_cities)]
df_filtered = df_filtered[
    (df_filtered['humedad'] >= humedad_range[0]) & 
    (df_filtered['humedad'] <= humedad_range[1])
]
df_filtered = df_filtered[
    (df_filtered['presion'] >= presion_range[0]) & 
    (df_filtered['presion'] <= presion_range[1])
]

# APLICACIÓN DEL FILTRO TEMPORAL
df_filtered = df_filtered[df_filtered['timestamp_registro'] >= cutoff_time]


# --- VISUALIZACIONES (Requisito 3 Visualizaciones - Instrucción 11) ---

latest_data = df_filtered.sort_values(by='timestamp_registro', ascending=False).drop_duplicates(subset=['ciudad_nombre'])

# --- VISUALIZACIONES (Mejora de Layout: 3 KPIs en Columnas) ---

# Crear 3 columnas para los indicadores
col1, col2, col3 = st.columns(3)

# 1. KPI: Temperatura Promedio
avg_temp = latest_data['temperatura_c'].mean() if not latest_data.empty else 0
col1.metric(label="🌡️ Temp. Promedio", value=f"{avg_temp:.2f} °C")

# 2. KPI: Humedad Promedio
avg_hum = latest_data['humedad'].mean() if not latest_data.empty else 0
col2.metric(label="💧 Humedad Promedio", value=f"{avg_hum:.1f} %")

# 3. KPI: Presión Promedio
avg_press = latest_data['presion'].mean() if not latest_data.empty else 0
col3.metric(label="🌬️ Presión Promedio", value=f"{avg_press:.0f} hPa")

# -------------------------------------------------------------

# 2. Visualización: Gráfica de Barras (Comparación de Humedad)
if not latest_data.empty:
    st.subheader("Humedad Actual por Ciudad")
    fig_humedad = px.bar(
        latest_data,
        x='ciudad_nombre',
        y='humedad',
        color='ciudad_nombre',
        labels={'humedad': 'Humedad (%)', 'ciudad_nombre': 'Ciudad'},
        template='seaborn'
    )
    st.plotly_chart(fig_humedad, use_container_width=True)

# 4. Visualización: Gráfica de Tendencia de Temperatura (Análisis temporal)
if not df_filtered.empty:
    st.subheader("Tendencia Histórica de Temperatura")
    fig_temp_line = px.line(
        df_filtered.sort_values(by='timestamp_registro'),
        x='timestamp_registro',
        y='temperatura_c',
        color='ciudad_nombre',
        title='Temperatura (°C) a lo largo del tiempo',
        labels={'temperatura_c': 'Temperatura (°C)', 'timestamp_registro': 'Tiempo'},
        template='plotly_white'
    )
    st.plotly_chart(fig_temp_line, use_container_width=True)

# 3. Visualización: Tabla Detallada
st.subheader("Datos de Clima Detallados")
st.dataframe(df_filtered[[
    'ciudad_nombre', 
    'timestamp_registro', 
    'temperatura_c', 
    'humedad', 
    'presion'
]].head(10), use_container_width=True)