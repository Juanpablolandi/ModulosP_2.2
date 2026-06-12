from pathlib import Path
from etl.config import BRONZE_MANUAL_DIR, BRONZE_RPA_DIR, ROOT_DIR
from etl.db import execute_sql_file, refresh_gold_views
from etl.load import append_df, attach_id_geo, attach_id_tiempo, log_file, already_processed
from etl.transform import bce, inec, supercias, mineduc


def init_database():
    execute_sql_file(ROOT_DIR / "sql" / "03_create_tables.sql")
    execute_sql_file(ROOT_DIR / "sql" / "04_gold_views.sql")


def detect_source(file_path):
    name = file_path.name.lower()
    if "pib_real" in name:
        return "pib_real"
    if "pib_nominal" in name or "percapita_nominal" in name:
        return "pib_nominal"
    if "vab" in name:
        return "vab"
    if "petroleo" in name or "riesgo" in name or "wti" in name:
        return "petroleo_riesgo"
    if "iee" in name or "expectativas" in name:
        return "iee"
    if "enemdu" in name or "empleo" in name:
        return "enemdu"
    if "censo" in name or "rama" in name:
        return "censo_actividad"
    if "ranking" in name or "supercias_ranking" in name:
        return "supercias_ranking"
    if "directorio" in name or "compan" in name or "compania" in name:
        return "supercias_directorio"
    if "amie" in name or "mineduc" in name:
        return "mineduc_amie"
    return "desconocido"


def process_file(file_path):
    source = detect_source(file_path)
    if source == "desconocido":
        log_file(file_path, source, "SKIP", "Nombre de archivo no reconocido")
        return

    try:
        if source == "pib_real":
            df_real = bce.transform_pib_real(file_path)
            df_real = attach_id_tiempo(df_real, "fecha")
            out = df_real[["id_tiempo", "pib_real_musd", "poblacion", "pib_percapita_real", "variacion_pib_pct"]]
            append_df(out, "fact_macro_anual")

        elif source == "pib_nominal":
            # Si ya existe el año del PIB real, se actualiza el campo nominal; si no existe, se inserta una fila nueva.
            df_nom = bce.transform_pib_nominal(file_path)
            df_nom = attach_id_tiempo(df_nom, "fecha")
            out = df_nom[["id_tiempo", "pib_percapita_nominal_usd"]].rename(columns={"pib_percapita_nominal_usd": "pib_percapita_nominal"})
            append_df(out, "fact_macro_anual")

        elif source == "vab":
            df = attach_id_geo(bce.transform_vab(file_path))
            append_df(df[["id_geo", "anio", "ciiu", "vab_miles_usd"]], "fact_vab_prov_ind")

        elif source == "petroleo_riesgo":
            df = bce.transform_petroleo_riesgo(file_path)
            append_df(df, "fact_indicadores_diarios")

        elif source == "iee":
            df = attach_id_tiempo(bce.transform_iee(file_path), "fecha")
            append_df(df[["id_tiempo", "iee_global", "comercio", "construccion", "manufactura"]], "fact_iee")

        elif source == "enemdu":
            df = inec.transform_enemdu(file_path).rename(columns={"nacional": "total_nacional", "urbana": "total_urbana", "rural": "total_rural"})
            append_df(df[["periodo", "anio", "indicador", "total_nacional", "total_urbana", "total_rural"]], "fact_empleo")

        elif source == "censo_actividad":
            df = attach_id_geo(inec.transform_censo_actividad(file_path))
            append_df(df[["id_geo", "anio", "sexo", "grupo_edad", "personas_ocupadas", "ciiu"]], "fact_censo_actividad")

        elif source == "supercias_ranking":
            df = attach_id_geo(supercias.transform_ranking(file_path))
            append_df(df[["ruc", "nombre", "situacion_legal", "ingresos", "activos", "id_geo", "ciiu"]], "fact_supercias_ranking")

        elif source == "supercias_directorio":
            df = attach_id_geo(supercias.transform_directorio(file_path))
            append_df(df[["ruc", "nombre", "situacion_legal", "id_geo"]], "fact_supercias_directorio")

        elif source == "mineduc_amie":
            df = attach_id_geo(mineduc.transform_amie(file_path))
            append_df(df[["anio_lectivo", "amie", "nombre_institucion", "id_geo", "nivel_educacion", "sostenimiento", "total_estudiantes", "es_bachillerato"]], "fact_mineduc_amie")

        log_file(file_path, source, "OK", "Archivo procesado correctamente")
    except Exception as exc:
        log_file(file_path, source, "ERROR", str(exc))
        raise


def run_pipeline(include_manual=True, include_rpa=True, only_new=True):
    folders = []
    if include_manual:
        folders.append(BRONZE_MANUAL_DIR)
    if include_rpa:
        folders.append(BRONZE_RPA_DIR)

    files = []
    for folder in folders:
        files.extend(Path(folder).glob("*.csv"))
        files.extend(Path(folder).glob("*.xlsx"))
        files.extend(Path(folder).glob("*.xls"))

    for file_path in sorted(files):
        if only_new and already_processed(file_path):
            continue
        process_file(file_path)

    refresh_gold_views()


if __name__ == "__main__":
    run_pipeline()
