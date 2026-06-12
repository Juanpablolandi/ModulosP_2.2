# Pipeline de Datos del Macroentorno Económico del Ecuador

## Descripción

Este repositorio contiene los componentes desarrollados para el segundo entregable del reto final de la asignatura de Datos correspondiente al sexto ciclo.

El objetivo del proyecto es recopilar, transformar y almacenar información proveniente de diferentes instituciones públicas del Ecuador para su posterior análisis mediante dashboards en Power BI.

La solución se implementa utilizando PostgreSQL como base de datos principal y una arquitectura de procesamiento por capas que permite organizar y preparar los datos para la generación de indicadores y visualizaciones.

---

## Alcance del proyecto

Para este entregable se trabajó con información proveniente de:

* Banco Central del Ecuador (BCE)
* Instituto Nacional de Estadística y Censos (INEC)
* Superintendencia de Compañías (SUPERCIAS)
* Ministerio de Educación (MINEDUC)

Los datos obtenidos son procesados mediante módulos ETL y almacenados en tablas diseñadas para análisis y generación de reportes.

---

## Estructura general

```text
reto_final_6to_ciclo/
│
├── data/
├── docs/
├── etl/
├── sql/
├── requirements.txt
├── .env.example
└── README.md
```

### Carpetas principales

#### data/

Contiene los archivos de entrada utilizados durante el proceso ETL.

#### docs/

Incluye la documentación del proyecto y la arquitectura propuesta en el primer entregable.

#### etl/

Contiene los scripts encargados de la extracción, transformación y carga de datos.

#### sql/

Almacena los scripts necesarios para la creación de la base de datos, tablas y vistas utilizadas en el proyecto.

---

## Fuentes de información

Las principales fuentes utilizadas son:

### Banco Central del Ecuador

* PIB real anual
* PIB per cápita
* Valor Agregado Bruto por provincia
* Precio del petróleo
* Riesgo país
* Índice de Expectativas Empresariales

### INEC

* Indicadores de empleo y desempleo (ENEMDU)
* Información del Censo 2022

### SUPERCIAS

* Ranking de empresas
* Directorio de compañías

### MINEDUC

* Información estadística AMIE

---

## Base de datos

El proyecto utiliza PostgreSQL como sistema gestor de bases de datos.

El modelo implementado incluye tablas de dimensiones y tablas de hechos que permiten organizar la información de forma adecuada para análisis posteriores.

Entre las principales estructuras se encuentran:

* Dimensión de tiempo
* Dimensión geográfica
* Información macroeconómica
* Indicadores laborales
* Información empresarial
* Datos educativos
* Registro de archivos procesados

---

## Ejecución del proceso ETL

Una vez configurada la conexión con PostgreSQL e instaladas las dependencias del proyecto, el proceso principal puede ejecutarse mediante:

```bash
python -m etl.pipeline
```

Este procedimiento realiza:

1. Lectura de archivos de entrada.
2. Limpieza y validación de datos.
3. Transformación de la información.
4. Carga en PostgreSQL.
5. Actualización de estructuras utilizadas para análisis.

---

## Integración con Power BI

Los datos procesados son consumidos desde Power BI mediante conexión directa a PostgreSQL.

A partir de esta información se desarrollan dashboards orientados al análisis de:

* Evolución económica.
* Mercado laboral.
* Relación entre educación y actividad empresarial.
* Indicadores del entorno productivo nacional.
