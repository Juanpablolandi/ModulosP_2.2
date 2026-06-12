import pandas as pd
from etl.utils.io import read_table
from etl.utils.cleaning import normalize_columns, clean_text, to_number, to_date


def transform_pib_real(path):
    df = normalize_columns(read_table(path))
    rename = {
        "anos": "anio",
        "ano": "anio",
        "pib_musd": "pib_real_musd",
        "pib_percapita": "pib_percapita_real",
        "variacion_pct": "variacion_pib_pct",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})
    required = ["anio", "pib_real_musd", "variacion_pib_pct"]
    for col in required:
        if col not in df.columns:
            df[col] = None
    df["fecha"] = pd.to_datetime(df["anio"].astype(str) + "-01-01", errors="coerce").dt.date
    df["pib_real_musd"] = to_number(df["pib_real_musd"])
    if "poblacion" in df.columns:
        df["poblacion"] = to_number(df["poblacion"])
    df["variacion_pib_pct"] = to_number(df["variacion_pib_pct"])
    return df[[c for c in ["fecha", "anio", "pib_real_musd", "poblacion", "pib_percapita_real", "variacion_pib_pct"] if c in df.columns]].drop_duplicates()


def transform_pib_nominal(path):
    df = normalize_columns(read_table(path))
    df = df.rename(columns={"periodo": "fecha"})
    if "pib_percapita_nominal_usd" not in df.columns:
        candidates = [c for c in df.columns if "percapita" in c and "nominal" in c]
        if candidates:
            df = df.rename(columns={candidates[0]: "pib_percapita_nominal_usd"})
    df["fecha"] = to_date(df["fecha"])
    df["anio"] = pd.to_datetime(df["fecha"]).dt.year
    df["pib_percapita_nominal_usd"] = to_number(df["pib_percapita_nominal_usd"])
    return df[["fecha", "anio", "pib_percapita_nominal_usd"]].drop_duplicates()


def transform_vab(path):
    df = normalize_columns(read_table(path))
    df = df.rename(columns={"ano": "anio", "a_o": "anio"})
    for col in ["provincia", "canton", "ciiu"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    if "vab_miles_usd" in df.columns:
        df["vab_miles_usd"] = to_number(df["vab_miles_usd"])
    return df[[c for c in ["anio", "cod_provincia", "provincia", "cod_canton", "canton", "ciiu", "vab_miles_usd"] if c in df.columns]].drop_duplicates()


def transform_petroleo_riesgo(path):
    df = normalize_columns(read_table(path))
    df = df.rename(columns={"periodo": "fecha"})
    df["fecha"] = to_date(df["fecha"])
    for col in ["precio_petroleo_wti", "riesgo_pais_pb"]:
        if col in df.columns:
            df[col] = to_number(df[col])
    return df[[c for c in ["fecha", "precio_petroleo_wti", "riesgo_pais_pb"] if c in df.columns]].drop_duplicates()


def transform_iee(path):
    df = normalize_columns(read_table(path))
    df["fecha"] = to_date(df["fecha"])
    for col in ["iee_global", "comercio", "construccion", "manufactura"]:
        if col in df.columns:
            df[col] = to_number(df[col])
    return df[[c for c in ["fecha", "iee_global", "comercio", "construccion", "manufactura"] if c in df.columns]].drop_duplicates()
