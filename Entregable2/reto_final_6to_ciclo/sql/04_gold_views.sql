DROP MATERIALIZED VIEW IF EXISTS gold_iee_coyuntura CASCADE;
DROP MATERIALIZED VIEW IF EXISTS gold_vab_sector_provincia CASCADE;
DROP MATERIALIZED VIEW IF EXISTS gold_bachilleres_vs_empresas CASCADE;
DROP MATERIALIZED VIEW IF EXISTS gold_empresas_provincia CASCADE;
DROP MATERIALIZED VIEW IF EXISTS gold_petroleo_30dias CASCADE;
DROP MATERIALIZED VIEW IF EXISTS gold_empleo_tendencia CASCADE;
DROP MATERIALIZED VIEW IF EXISTS gold_pib_tendencia CASCADE;

-- Vista Gold base: evolución del PIB con clasificación de ciclo económico.
CREATE MATERIALIZED VIEW gold_pib_tendencia AS
SELECT
    t.anio,
    m.pib_real_musd,
    m.pib_percapita_nominal,
    m.variacion_pib_pct,
    CASE
        WHEN m.variacion_pib_pct > 2 THEN 'Crecimiento fuerte'
        WHEN m.variacion_pib_pct > 0 THEN 'Crecimiento moderado'
        WHEN m.variacion_pib_pct = 0 THEN 'Estancamiento'
        ELSE 'Contracción'
    END AS clasificacion
FROM fact_macro_anual m
JOIN dim_tiempo t ON t.id_tiempo = m.id_tiempo
ORDER BY t.anio;

-- TODO base implementado: tasa de desempleo trimestral histórica.
CREATE MATERIALIZED VIEW gold_empleo_tendencia AS
SELECT
    periodo,
    anio,
    indicador,
    total_nacional,
    total_urbana,
    total_rural
FROM fact_empleo
WHERE indicador ILIKE '%DESEMPLEO%'
ORDER BY anio, periodo;

-- TODO base implementado: promedio móvil de 30 días del WTI.
CREATE MATERIALIZED VIEW gold_petroleo_30dias AS
SELECT
    fecha,
    precio_petroleo_wti,
    riesgo_pais_pb,
    AVG(precio_petroleo_wti) OVER (ORDER BY fecha ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS wti_promedio_30dias
FROM fact_indicadores_diarios
WHERE precio_petroleo_wti IS NOT NULL
ORDER BY fecha;

-- TODO base implementado: empresas activas e ingresos por provincia.
CREATE MATERIALIZED VIEW gold_empresas_provincia AS
SELECT
    g.provincia,
    COUNT(DISTINCT d.ruc) FILTER (WHERE d.situacion_legal ILIKE '%ACTIVA%') AS empresas_activas,
    COUNT(DISTINCT r.ruc) AS empresas_ranking,
    COALESCE(SUM(r.ingresos), 0) AS ingresos_totales,
    COALESCE(SUM(r.activos), 0) AS activos_totales
FROM dim_geografia g
LEFT JOIN fact_supercias_directorio d ON d.id_geo = g.id_geo
LEFT JOIN fact_supercias_ranking r ON r.id_geo = g.id_geo
GROUP BY g.provincia
ORDER BY empresas_activas DESC;

-- TODO base implementado: cruce MINEDUC + Supercias por provincia.
CREATE MATERIALIZED VIEW gold_bachilleres_vs_empresas AS
WITH bachilleres AS (
    SELECT g.provincia, SUM(m.total_estudiantes) AS total_bachilleres
    FROM fact_mineduc_amie m
    JOIN dim_geografia g ON g.id_geo = m.id_geo
    WHERE m.es_bachillerato = TRUE
    GROUP BY g.provincia
), empresas AS (
    SELECT provincia, empresas_activas, ingresos_totales
    FROM gold_empresas_provincia
)
SELECT
    b.provincia,
    b.total_bachilleres,
    COALESCE(e.empresas_activas, 0) AS empresas_activas,
    COALESCE(e.ingresos_totales, 0) AS ingresos_totales,
    CASE
        WHEN COALESCE(e.empresas_activas, 0) = 0 THEN NULL
        ELSE ROUND(b.total_bachilleres / e.empresas_activas, 2)
    END AS bachilleres_por_empresa
FROM bachilleres b
LEFT JOIN empresas e ON e.provincia = b.provincia
ORDER BY bachilleres_por_empresa DESC NULLS LAST;

-- Vista Gold adicional 1 solicitada para 6to ciclo: VAB por sector y provincia.
CREATE MATERIALIZED VIEW gold_vab_sector_provincia AS
SELECT
    v.anio,
    g.provincia,
    v.ciiu,
    SUM(v.vab_miles_usd) AS vab_miles_usd
FROM fact_vab_prov_ind v
JOIN dim_geografia g ON g.id_geo = v.id_geo
GROUP BY v.anio, g.provincia, v.ciiu
ORDER BY v.anio DESC, vab_miles_usd DESC;

-- Vista Gold adicional 2 solicitada para 6to ciclo: coyuntura IEE mensual.
CREATE MATERIALIZED VIEW gold_iee_coyuntura AS
SELECT
    t.fecha,
    t.anio,
    t.mes,
    i.iee_global,
    i.comercio,
    i.construccion,
    i.manufactura,
    CASE
        WHEN i.iee_global >= 100 THEN 'Expectativa favorable'
        ELSE 'Expectativa débil'
    END AS lectura_coyuntura
FROM fact_iee i
JOIN dim_tiempo t ON t.id_tiempo = i.id_tiempo
ORDER BY t.fecha;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO macro_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO macro_etl;
