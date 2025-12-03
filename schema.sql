-- schema.sql
-- Este archivo crea la estructura de nuestras tablas.

-- 1. Tabla de DIMENSIÓN: DIM_CIUDADES (Datos de las ciudades)
CREATE TABLE IF NOT EXISTS DIM_CIUDADES (
    id_ciudad INTEGER PRIMARY KEY, -- Clave principal (identificador único)
    nombre TEXT NOT NULL,
    pais TEXT NOT NULL,
    latitud REAL,
    longitud REAL,
    UNIQUE(nombre, pais)
);

-- 2. Tabla de HECHOS: FACT_PRONOSTICO (Datos de las mediciones de clima)
CREATE TABLE IF NOT EXISTS FACT_PRONOSTICO (
    id_pronostico INTEGER PRIMARY KEY AUTOINCREMENT,
    ciudad_id INTEGER NOT NULL, -- Clave Foránea (FK): Conecta a DIM_CIUDADES
    timestamp_registro TEXT NOT NULL,
    temperatura_c REAL,
    temperatura_min_c REAL, 
    temperatura_max_c REAL,
    humedad INTEGER,
    presion INTEGER,
    descripcion_clima TEXT,
    FOREIGN KEY (ciudad_id) REFERENCES DIM_CIUDADES(id_ciudad)
);