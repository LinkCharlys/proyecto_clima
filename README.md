Proyecto de Ingeniería de Datos: Análisis del Clima Urbano

1. Descripción y Caso de Uso

Tema

Pipeline ETL y Dashboard de Visualización para el Monitoreo de Condiciones Climáticas Urbanas.

Caso de Uso

Este proyecto simula un proceso de Ingesta y Análisis de Datos en tiempo casi real. El objetivo es extraer información climática actual (temperatura, humedad, presión) para un conjunto de ciudades globales desde una API pública (WeatherAPI), transformarla, cargarla en una base de datos relacional (SQLite) y, finalmente, visualizar las tendencias históricas y los indicadores clave (KPIs) en un dashboard interactivo desarrollado en Streamlit.

Fuente de Datos

Tipo: API REST pública (WeatherAPI).

Variables Principales: Nombre de la ciudad, país, coordenadas, temperatura en °C, humedad (%), presión (hPa) y marca de tiempo (timestamp).

2. Modelo de Datos (Diagrama Simple)

El proyecto utiliza un esquema de estrella simple para el almacenamiento de datos, optimizado para el análisis de series de tiempo.

Tabla

Tipo

Descripción

Clave Primaria (PK)

Clave Foránea (FK)

DIM_CIUDADES

Dimensión

Almacena las características estáticas de las ciudades (nombre, país, latitud, longitud).

id_ciudad

-

FACT_PRONOSTICO

Hechos

Almacena las mediciones de clima en cada momento de la ejecución. Es la tabla que acumula el historial.

id_pronostico

ciudad_id $\to$ DIM_CIUDADES

3. Guía de Instalación y Configuración

A. Instalación de Dependencias

Se requiere Python 3.9+ y el gestor de paquetes pip.

Clonar el repositorio: (Asumiendo que es un repositorio)

git clone [URL_DEL_REPOSITORIO]
cd proyecto_clima





Crear y Activar el Entorno Virtual (venv):

python3 -m venv venv
source venv/bin/activate





Instalar librerías necesarias:

¡Importante! Instala todas las dependencias del proyecto usando el archivo requirements.txt recién creado:

pip install -r requirements.txt




B. Configuración de la API Key

La clave de la API y la lista de ciudades se gestionan a través de un archivo de configuración para mantener el código limpio.

Abre el archivo config.toml.

Reemplaza el valor de key con tu clave de API de WeatherAPI.

# config.toml
[api]
key = "TU_CLAVE_AQUI" 
base_url = "[http://api.weatherapi.com/v1/current.json](http://api.weatherapi.com/v1/current.json)"

[ciudades]
lista = ["Seoul", "Mexico City", "Beijing", "Tokyo", "Taipei"]




4. Ejecución del Pipeline ETL y Dashboard

Para simplificar la operación, se utiliza un script de shell (.sh) que automatiza todo el proceso:

Activa el entorno virtual.

Ejecuta el ETL (python main_etl.py) tres veces para acumular datos históricos, lo cual es necesario para dibujar la "Tendencia Histórica".

Lanza el dashboard de Streamlit.

A. Dar Permisos de Ejecución

Asegúrate de que el script tenga permisos para ejecutarse:

chmod +x run_full_pipeline.sh





B. Ejecutar el Pipeline Maestro

Ejecuta el script desde la carpeta principal del proyecto:

./run_full_pipeline.sh





C. Verificar

La Terminal mostrará los mensajes de las tres ejecuciones del ETL.

El archivo de base de datos clima_db.sqlite se creará/actualizará automáticamente.

El dashboard de Streamlit se abrirá en tu navegador web (http://localhost:8501), mostrando las visualizaciones con el historial de las últimas 48 horas por defecto.