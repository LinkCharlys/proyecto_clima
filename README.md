# Proyecto de Ingeniería de Datos: **Análisis del Clima Urbano**

Este repositorio contiene un pipeline ETL completo y un dashboard interactivo para monitorear condiciones climáticas urbanas en tiempo casi real. El sistema extrae datos desde una API pública, los transforma, los almacena en una base de datos relacional y finalmente los visualiza de forma clara y accesible.

---

## **1. Descripción del Proyecto**

### **Objetivo General**

Construir un flujo automatizado de **Extracción, Transformación y Carga (ETL)** para recopilar información climática de diferentes ciudades alrededor del mundo, almacenarla como historial y visualizarla mediante un dashboard.

### **Caso de Uso**

Este proyecto simula un proceso real de **monitoreo ambiental** en ciudades globales. Cada ejecución registra condiciones actuales como:

* Temperatura (°C)
* Humedad (%)
* Presión atmosférica (hPa)
* Hora de la medición

Los datos se almacenan de forma histórica para analizar tendencias de corto plazo.

### **Fuente de Datos**

* **Tipo:** API REST pública
* **Proveedor:** WeatherAPI
* **Variables principales:** ciudad, país, coordenadas, temperatura, humedad, presión y timestamp.

---

##  **2. Modelo de Datos (Esquema Simplificado)**

El sistema utiliza un modelo tipo **estrella (Star Schema)**, pensado para análisis de series de tiempo.

| Tabla               | Tipo      | Descripción                                                            | PK            | FK                       |
| ------------------- | --------- | ---------------------------------------------------------------------- | ------------- | ------------------------ |
| **DIM_CIUDADES**    | Dimensión | Información estática de cada ciudad (nombre, país, latitud, longitud). | id_ciudad     | -                        |
| **FACT_PRONOSTICO** | Hechos    | Registra cada medición del clima. Almacena el historial.               | id_pronostico | ciudad_id → DIM_CIUDADES |

Este diseño permite consultar mediciones por ciudad, generar gráficos históricos y analizar tendencias.

---

##  **3. Instalación y Configuración**

### **A. Clonar el repositorio**

```bash
git clone [URL_DEL_REPOSITORIO]
cd proyecto_clima
```

### **B. Crear y activar entorno virtual (venv)**

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# .\venv\Scripts\activate  # Windows
```

### **C. Instalar dependencias**

El proyecto incluye un archivo `requirements.txt` con todas las librerías necesarias.

```bash
pip install -r requirements.txt
```

---

##  **4. Configurar la API Key**

El acceso a la API requiere una clave personal de WeatherAPI.

1. Abre el archivo **config.toml**.
2. Sustituye el valor de `key` por tu API Key.

Ejemplo:

```toml
[api]
key = "TU_CLAVE_AQUI"
base_url = "http://api.weatherapi.com/v1/current.json"

[ciudades]
lista = ["Seoul", "Mexico City", "Beijing", "Tokyo", "Taipei"]
```

Puedes agregar o quitar ciudades según tus necesidades.

---

##  **5. Ejecución del Pipeline ETL y Dashboard**

Para simplificar todo el proceso, el proyecto incluye el script automatizado **run_full_pipeline.sh**, que:

* Activa el entorno virtual.
* Ejecuta el ETL tres veces para generar historial.
* Lanza el dashboard de Streamlit automáticamente.

### **A. Dar permisos de ejecución al script**

```bash
chmod +x run_full_pipeline.sh
```

### **B. Ejecutar el pipeline maestro**

```bash
./run_full_pipeline.sh
```

### **C. Verificación**

* La terminal mostrará la salida de cada ejecución del ETL.
* Se generará/actualizará la base de datos **clima_db.sqlite**.
* El dashboard abrirá en el navegador:
  **[http://localhost:8501](http://localhost:8501)**

En el dashboard podrás visualizar:

* Temperatura actual por ciudad
* Humedad y presión
* Tendencia histórica (acumulada por las corridas del ETL)
* KPIs clave

---

## **Estructura del Proyecto**

```
├── dashboard.py
├── extract.py
├── transform.py
├── load.py
├── main_etl.py
├── run_full_pipeline.sh
├── schema.sql
├── requirements.txt
├── README.md
└── config.toml
```

---

##  **Notas Finales**

* Este proyecto es ideal para prácticas de Ingeniería de Datos, automatización y visualización.
* WeatherAPI cuenta con un plan gratuito suficiente para pruebas.
* La base de datos crece con cada ejecución, permitiendo análisis históricos.

Si deseas extender este proyecto, algunas ideas son:

* Integrar almacenamiento en la nube (AWS S3, BigQuery, PostgreSQL, etc.)
* Agregar monitoreo con Prometheus/Grafana
* Ejecutar el ETL en un cron job automatizado

---

¡Gracias por revisar este proyecto!
Si te es útil, no olvides dejar una ⭐ en GitHub.
