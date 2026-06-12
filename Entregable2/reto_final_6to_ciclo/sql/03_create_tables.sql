CREATE SCHEMA IF NOT EXISTS public;

DROP TABLE IF EXISTS file_processing_log CASCADE;
DROP TABLE IF EXISTS fact_mineduc_amie CASCADE;
DROP TABLE IF EXISTS fact_supercias_directorio CASCADE;
DROP TABLE IF EXISTS fact_supercias_ranking CASCADE;
DROP TABLE IF EXISTS fact_censo_actividad CASCADE;
DROP TABLE IF EXISTS fact_empleo CASCADE;
DROP TABLE IF EXISTS fact_vab_prov_ind CASCADE;
DROP TABLE IF EXISTS fact_iee CASCADE;
DROP TABLE IF EXISTS fact_indicadores_diarios CASCADE;
DROP TABLE IF EXISTS fact_macro_anual CASCADE;
DROP TABLE IF EXISTS dim_tiempo CASCADE;
DROP TABLE IF EXISTS dim_geografia CASCADE;

CREATE TABLE dim_geografia (
    id_geo SERIAL PRIMARY KEY,
    provincia VARCHAR(60) NOT NULL,
    cod_provincia INTEGER,
    canton VARCHAR(80),
    cod_canton INTEGER,
    CONSTRAINT uq_dim_geografia UNIQUE (provincia, canton, cod_provincia, cod_canton)
);

CREATE TABLE dim_tiempo (
    id_tiempo SERIAL PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    anio INTEGER NOT NULL,
    mes INTEGER,
    trimestre INTEGER
);

CREATE TABLE fact_macro_anual (
    id SERIAL PRIMARY KEY,
    id_tiempo INTEGER REFERENCES dim_tiempo(id_tiempo),
    pib_real_musd NUMERIC(14,2),
    poblacion NUMERIC(14,0),
    pib_percapita_real NUMERIC(10,2),
    pib_percapita_nominal NUMERIC(10,2),
    variacion_pib_pct NUMERIC(6,3)
);

CREATE TABLE fact_indicadores_diarios (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    precio_petroleo_wti NUMERIC(8,2),
    riesgo_pais_pb INTEGER
);

CREATE TABLE fact_iee (
    id SERIAL PRIMARY KEY,
    id_tiempo INTEGER REFERENCES dim_tiempo(id_tiempo),
    iee_global NUMERIC(10,2),
    comercio NUMERIC(10,2),
    construccion NUMERIC(10,2),
    manufactura NUMERIC(10,2)
);

CREATE TABLE fact_vab_prov_ind (
    id SERIAL PRIMARY KEY,
    id_geo INTEGER REFERENCES dim_geografia(id_geo),
    anio INTEGER NOT NULL,
    ciiu VARCHAR(30),
    vab_miles_usd NUMERIC(16,2)
);

CREATE TABLE fact_empleo (
    id SERIAL PRIMARY KEY,
    periodo VARCHAR(30) NOT NULL,
    anio INTEGER,
    indicador VARCHAR(120) NOT NULL,
    total_nacional NUMERIC(14,2),
    total_urbana NUMERIC(14,2),
    total_rural NUMERIC(14,2)
);

CREATE TABLE fact_censo_actividad (
    id SERIAL PRIMARY KEY,
    id_geo INTEGER REFERENCES dim_geografia(id_geo),
    anio INTEGER DEFAULT 2022,
    sexo VARCHAR(30),
    grupo_edad VARCHAR(60),
    personas_ocupadas NUMERIC(14,0),
    ciiu VARCHAR(30)
);

CREATE TABLE fact_supercias_ranking (
    id SERIAL PRIMARY KEY,
    ruc VARCHAR(20),
    nombre VARCHAR(250),
    situacion_legal VARCHAR(80),
    ingresos NUMERIC(18,2),
    activos NUMERIC(18,2),
    id_geo INTEGER REFERENCES dim_geografia(id_geo),
    ciiu VARCHAR(30)
);

CREATE TABLE fact_supercias_directorio (
    id SERIAL PRIMARY KEY,
    ruc VARCHAR(20),
    nombre VARCHAR(250),
    situacion_legal VARCHAR(80),
    id_geo INTEGER REFERENCES dim_geografia(id_geo)
);

CREATE TABLE fact_mineduc_amie (
    id SERIAL PRIMARY KEY,
    anio_lectivo VARCHAR(20),
    amie VARCHAR(30),
    nombre_institucion VARCHAR(250),
    id_geo INTEGER REFERENCES dim_geografia(id_geo),
    nivel_educacion VARCHAR(120),
    sostenimiento VARCHAR(80),
    total_estudiantes NUMERIC(14,0),
    es_bachillerato BOOLEAN DEFAULT FALSE
);

CREATE TABLE file_processing_log (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(250) NOT NULL,
    file_path TEXT NOT NULL,
    source_name VARCHAR(80) NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) NOT NULL,
    message TEXT,
    CONSTRAINT uq_file_processing UNIQUE (file_path)
);

CREATE INDEX idx_dim_geografia_provincia ON dim_geografia(provincia);
CREATE INDEX idx_fact_vab_anio ON fact_vab_prov_ind(anio);
CREATE INDEX idx_fact_empleo_indicador ON fact_empleo(indicador);
CREATE INDEX idx_fact_mineduc_bachillerato ON fact_mineduc_amie(es_bachillerato);
CREATE INDEX idx_fact_supercias_situacion ON fact_supercias_directorio(situacion_legal);
