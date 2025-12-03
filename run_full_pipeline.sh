#!/bin/bash

# Este script activa el entorno virtual, corre el ETL 3 veces para historial, y lanza el dashboard.

# 1. Activar el entorno virtual (IMPORTANTE)
source venv/bin/activate

# 2. Definir cuántas veces correr el ETL (para acumular historial)
RUNS=3 
echo "--- Iniciando pipeline completo. El ETL se ejecutará $RUNS veces para acumular historial. ---"

# 3. Correr el ETL en un bucle
for i in $(seq 1 $RUNS); do
    echo "Ejecución ETL número $i de $RUNS..."
    
    # El ETL ya tiene la lógica de ignorar la inserción de DIM_CIUDADES si ya existe.
    python main_etl.py
    
    # Opcional: Pausa entre ejecuciones para que las marcas de tiempo sean diferentes
    sleep 5 
done

# 4. Iniciar el Dashboard de Streamlit
echo "--- Datos acumulados. Lanzando el Dashboard de Streamlit. ---"
streamlit run dashboard/dashboard.py