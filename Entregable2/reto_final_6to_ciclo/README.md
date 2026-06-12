# Pipeline de datos del macroentorno ecuatoriano — Reto final 6to ciclo

Repositorio base para el **segundo entregable** del reto final de Datos: **módulos ETL, DDL SQL y README**.

El proyecto implementa la arquitectura medallón definida en el primer entregable: **Bronze → ETL → Silver → Gold → Power BI**. Está enfocado únicamente en **6to ciclo**, por lo que usa **PostgreSQL**, contempla los **tres bloques completos de fuentes**, incluye **mínimo doce tablas Silver**, usa **vistas materializadas Gold** y deja preparado el mecanismo de detección de archivos nuevos provenientes del equipo de RPA.

---

## 1. Alcance del reto de 6to ciclo

Según el documento del reto final, el nivel de 6to ciclo debe trabajar con:

- **Base de datos:** PostgreSQL.
- **Fuentes:** los tres bloques completos: BCE, INEC, Supercias y MINEDUC.
- **Tablas Silver:** mínimo doce tablas.
- **Vistas Gold:** las cuatro vistas base más dos vistas adicionales propuestas y justificadas.
- **Dashboard:** tres páginas con KPIs, visualizaciones y análisis ejecutivo por página.
- **Integración RPA:** detección de archivos nuevos en la carpeta definida para RPA.

---

## 2. Estructura del repositorio

```text
reto_final_6to_ciclo/
├── data/
│   ├── bronze/
│   │   ├── manual/          # Archivos descargados manualmente semanas 1-4
│   │   └── rpa/             # Archivos depositados por RPA semanas 5-7
│   └── silver_exports/      # Exportaciones opcionales de control
├── docs/
│   ├── arquitectura_entregable_1.png
│   ├── RETO_FINAL_DATOS.pdf
│   ├── decisiones_limpieza.md
│   └── estructura_archivos_fuente.md
├── etl/
│   ├── config.py
│   ├── db.py
│   ├── load.py
│   ├── pipeline.py
│   ├── rpa_watch.py
│   ├── transform/
│   │   ├── bce.py
│   │   ├── inec.py
│   │   ├── supercias.py
│   │   └── mineduc.py
│   └── utils/
│       ├── cleaning.py
│       └── io.py
├── sql/
│   ├── 01_create_database.sql
│   ├── 02_create_roles.sql
│   ├── 03_create_tables.sql
│   ├── 04_gold_views.sql
│   └── 05_refresh_gold_views.sql
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 3. Fuentes contempladas

| Bloque | Fuente | Módulo ETL | Tabla Silver principal |
|---|---|---|---|
| BCE | PIB real anual | `etl/transform/bce.py` | `fact_macro_anual` |
| BCE | PIB per cápita nominal | `etl/transform/bce.py` | `fact_macro_anual` |
| BCE | VAB por provincia e industria | `etl/transform/bce.py` | `fact_vab_prov_ind` |
| BCE | Precio petróleo y riesgo país | `etl/transform/bce.py` | `fact_indicadores_diarios` |
| BCE | IEE Expectativas Empresariales | `etl/transform/bce.py` | `fact_iee` |
| INEC | ENEMDU indicadores laborales | `etl/transform/inec.py` | `fact_empleo` |
| INEC | Censo 2022 rama de actividad | `etl/transform/inec.py` | `fact_censo_actividad` |
| Supercias | Ranking de empresas | `etl/transform/supercias.py` | `fact_supercias_ranking` |
| Supercias | Directorio de compañías | `etl/transform/supercias.py` | `fact_supercias_directorio` |
| MINEDUC | AMIE 2023-2024 | `etl/transform/mineduc.py` | `fact_mineduc_amie` |

Además, el modelo incluye `dim_geografia`, `dim_tiempo` y `file_processing_log` para normalización y control del reprocesamiento.

---

## 4. Modelo Silver implementado

El script `sql/03_create_tables.sql` crea las siguientes tablas:

1. `dim_geografia`
2. `dim_tiempo`
3. `fact_macro_anual`
4. `fact_indicadores_diarios`
5. `fact_iee`
6. `fact_vab_prov_ind`
7. `fact_empleo`
8. `fact_censo_actividad`
9. `fact_supercias_ranking`
10. `fact_supercias_directorio`
11. `fact_mineduc_amie`
12. `file_processing_log`

Con esto se cumple el requisito de 6to ciclo de trabajar con **mínimo doce tablas Silver**.

---

## 5. Vistas Gold implementadas

El script `sql/04_gold_views.sql` crea vistas materializadas para análisis y conexión con Power BI:

| Vista Gold | Propósito | Pregunta del dashboard |
|---|---|---|
| `gold_pib_tendencia` | Evolución del PIB y clasificación del ciclo económico | P1 |
| `gold_empleo_tendencia` | Tendencia histórica de desempleo | P2 |
| `gold_petroleo_30dias` | Promedio móvil de 30 días del WTI | P1 / contexto macro |
| `gold_empresas_provincia` | Empresas activas e ingresos por provincia | P3 |
| `gold_bachilleres_vs_empresas` | Cruce de bachilleres y empresas activas por provincia | P3 |
| `gold_vab_sector_provincia` | Vista adicional 6to ciclo: VAB por sector y provincia | P2 |
| `gold_iee_coyuntura` | Vista adicional 6to ciclo: expectativas empresariales recientes | P1 |

Las dos vistas adicionales propuestas para 6to ciclo son:

- `gold_vab_sector_provincia`: permite analizar concentración económica por provincia y sector CIIU.
- `gold_iee_coyuntura`: agrega contexto mensual de expectativas empresariales para interpretar el ciclo económico.

---

## 6. Instalación del entorno

### 6.1 Crear entorno virtual

```bash
python -m venv .venv
```

Activar en Windows:

```bash
.venv\Scripts\activate
```

Activar en Linux/Mac:

```bash
source .venv/bin/activate
```

### 6.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 6.3 Configurar variables de entorno

Copiar `.env.example` como `.env`:

```bash
copy .env.example .env
```

En Linux/Mac:

```bash
cp .env.example .env
```

Editar `.env` con los datos reales de PostgreSQL.

---

## 7. Preparar PostgreSQL

### 7.1 Crear base de datos

Entrar a PostgreSQL con un usuario administrador y ejecutar:

```sql
\i sql/01_create_database.sql
```

Luego conectarse a la base:

```sql
\c macroentorno_ecuador
```

### 7.2 Crear roles

```sql
\i sql/02_create_roles.sql
```

### 7.3 Crear tablas Silver y vistas Gold

```sql
\i sql/03_create_tables.sql
\i sql/04_gold_views.sql
```

---

## 8. Ubicación de archivos Bronze

Durante semanas 1 a 4, colocar archivos descargados manualmente en:

```text
data/bronze/manual/
```

Desde semana 5, el equipo de RPA debe depositar archivos en:

```text
data/bronze/rpa/
```

El formato recomendado es:

```text
fuente_YYYYMMDD.ext
```

Ejemplos:

```text
pib_real_20260512.xlsx
pib_nominal_20260512.xlsx
vab_20260512.xlsx
petroleo_riesgo_20260512.xlsx
iee_20260512.xlsx
enemdu_20260512.xlsx
censo_actividad_20260512.xlsx
supercias_ranking_20260512.csv
supercias_directorio_20260512.csv
mineduc_amie_20260512.csv
```

---

## 9. Ejecutar el pipeline ETL

Desde la raíz del repositorio:

```bash
python -m etl.pipeline
```

Este comando realiza lo siguiente:

1. Busca archivos `.csv`, `.xlsx` y `.xls` en las carpetas Bronze.
2. Detecta la fuente según el nombre del archivo.
3. Aplica limpieza y normalización.
4. Carga dimensiones y tablas de hechos Silver.
5. Registra cada archivo procesado en `file_processing_log`.
6. Refresca las vistas materializadas Gold.

---

## 10. Ejecutar detección automática de RPA

Para dejar el pipeline escuchando archivos nuevos del equipo de RPA:

```bash
python -m etl.rpa_watch
```

Cuando RPA copie un archivo nuevo en `data/bronze/rpa/`, el pipeline lo procesa automáticamente y refresca las vistas Gold.

---

## 11. Conexión con Power BI

En Power BI:

1. Seleccionar **Obtener datos**.
2. Elegir **PostgreSQL database**.
3. Ingresar servidor, base de datos y usuario de lectura.
4. Conectar principalmente a las vistas Gold:
   - `gold_pib_tendencia`
   - `gold_empleo_tendencia`
   - `gold_petroleo_30dias`
   - `gold_empresas_provincia`
   - `gold_bachilleres_vs_empresas`
   - `gold_vab_sector_provincia`
   - `gold_iee_coyuntura`

---

## 12. Páginas sugeridas del dashboard

### Página P1 — Evolución económica

Usar:

- `gold_pib_tendencia`
- `gold_petroleo_30dias`
- `gold_iee_coyuntura`

Visualizaciones:

- Línea de PIB real anual.
- Barras de variación del PIB por clasificación.
- KPI de último PIB per cápita nominal.
- Línea de IEE mensual como contexto.

### Página P2 — Actividad económica y empleo

Usar:

- `gold_empleo_tendencia`
- `gold_vab_sector_provincia`
- `fact_censo_actividad` si se desea análisis más detallado por CIIU.

Visualizaciones:

- Mapa de VAB por provincia.
- Top 10 sectores CIIU.
- KPI de tasa de desempleo más reciente.

### Página P3 — Bachilleres vs empresas

Usar:

- `gold_bachilleres_vs_empresas`
- `gold_empresas_provincia`

Visualizaciones:

- Barras agrupadas: bachilleres vs empresas activas.
- Tabla de ratio bachilleres por empresa.
- KPI de total nacional de bachilleres.

---

## 13. Estado del entregable

Este repositorio cubre el **segundo entregable**:

- Módulos ETL por fuente.
- DDL SQL de PostgreSQL.
- Vistas Gold materializadas.
- README con instalación, ejecución, carpetas y conexión con Power BI.
- Carpeta para integración RPA.
- Documentación de limpieza y estructura esperada de archivos.

Los archivos reales de las fuentes no se incluyen en el repositorio porque deben ser descargados o recibidos desde RPA.
