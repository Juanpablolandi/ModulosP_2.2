# Nombres esperados de archivos fuente

El pipeline detecta la fuente por palabras clave en el nombre del archivo. Se recomienda usar el formato acordado con RPA: `fuente_YYYYMMDD.ext`.

| Fuente | Ejemplo de nombre | Carpeta inicial |
|---|---|---|
| PIB real anual | `pib_real_20260512.xlsx` | `data/bronze/manual` o `data/bronze/rpa` |
| PIB per cápita nominal | `pib_nominal_20260512.xlsx` | `data/bronze/manual` o `data/bronze/rpa` |
| VAB por provincia e industria | `vab_20260512.xlsx` | `data/bronze/manual` o `data/bronze/rpa` |
| Petróleo y riesgo país | `petroleo_riesgo_20260512.xlsx` | `data/bronze/manual` o `data/bronze/rpa` |
| IEE | `iee_20260512.xlsx` | `data/bronze/manual` o `data/bronze/rpa` |
| ENEMDU | `enemdu_20260512.xlsx` | `data/bronze/manual` o `data/bronze/rpa` |
| Censo rama actividad | `censo_actividad_20260512.xlsx` | `data/bronze/manual` o `data/bronze/rpa` |
| Supercias Ranking | `supercias_ranking_20260512.csv` | `data/bronze/manual` o `data/bronze/rpa` |
| Supercias Directorio | `supercias_directorio_20260512.csv` | `data/bronze/manual` o `data/bronze/rpa` |
| MINEDUC AMIE | `mineduc_amie_20260512.csv` | `data/bronze/manual` o `data/bronze/rpa` |

Si el nombre no contiene una palabra clave reconocida, el archivo se registra como `SKIP` en `file_processing_log`.
