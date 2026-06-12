# Decisiones de limpieza — Reto final Datos 6to ciclo

Este documento resume las decisiones iniciales de limpieza para el segundo entregable del repositorio.

## Reglas generales

1. **Renombrado de columnas:** todas las columnas se convierten a minúsculas, sin tildes y con guion bajo. Ejemplo: `AÑO` pasa a `anio` y `Variacion_pct` pasa a `variacion_pct`.
2. **Nulos:** no se reemplazan por cero de forma automática. Se mantienen como `NULL` cuando representan ausencia de dato real. Solo se usa cero en agregaciones Gold cuando el cálculo lo requiere, por ejemplo empresas activas no encontradas por provincia.
3. **Duplicados:** se eliminan registros duplicados completos antes de cargar cada tabla de hechos.
4. **Tipos de datos:** fechas a `DATE`, años a `INTEGER`, montos a `NUMERIC`, textos geográficos a mayúsculas sin tildes.
5. **Normalización geográfica:** provincia y cantón se centralizan en `dim_geografia` para cruzar VAB, Censo, Supercias y MINEDUC.
6. **Dimensión temporal:** las fuentes con fecha se enlazan con `dim_tiempo` para facilitar filtros por año, mes y trimestre.

## Reglas por fuente

| Fuente | Limpieza principal | Tabla Silver destino |
|---|---|---|
| PIB real anual | Mantener el primer año aunque tenga variación nula; convertir año a fecha 01-01 | `fact_macro_anual` |
| PIB per cápita nominal | Convertir `Periodo` a fecha y tomar año | `fact_macro_anual` |
| VAB provincia-industria | Normalizar provincia, cantón y CIIU; cruzar con `dim_geografia` | `fact_vab_prov_ind` |
| Petróleo y riesgo país | Convertir frecuencia diaria a `DATE`; normalizar valores numéricos | `fact_indicadores_diarios` |
| IEE | Convertir `Fecha` a `DATE`; cargar indicadores mensuales | `fact_iee` |
| ENEMDU | Mantener indicador por fila y áreas nacional/urbana/rural como columnas numéricas | `fact_empleo` |
| Censo 2022 | Carga estática; normalizar provincia, cantón, sexo, edad y CIIU | `fact_censo_actividad` |
| Supercias Ranking | Normalizar RUC, situación legal, provincia, CIIU, ingresos y activos | `fact_supercias_ranking` |
| Supercias Directorio | Contar empresas activas por provincia | `fact_supercias_directorio` |
| MINEDUC AMIE | Leer CSV con `sep=';'` y `latin-1`; marcar Bachillerato para P3 | `fact_mineduc_amie` |
