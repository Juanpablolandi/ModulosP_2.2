import pandas as pd
from etl.utils.io import read_table
from etl.utils.cleaning import normalize_columns, clean_text, to_number


def transform_enemdu(path):
    df = normalize_columns(read_table(path))
    # El documento indica estructura pivotada: indicador por fila y áreas como columnas.
    df = df.rename(columns={"indicadores": "indicador"})
    for col in ["encuesta", "periodo", "indicador"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    if "periodo" in df.columns:
        df["anio"] = df["periodo"].astype(str).str.extract(r"(20\d{2})").astype(float)
    for col in ["nacional", "urbana", "rural"]:
        if col in df.columns:
            df[col] = to_number(df[col])
    return df[[c for c in ["encuesta", "periodo", "anio", "indicador", "nacional", "urbana", "rural"] if c in df.columns]].drop_duplicates()


def transform_censo_actividad(path):
    df = normalize_columns(read_table(path))
    for col in ["provincia", "canton", "sexo", "grupo_edad", "ciiu"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    if "personas_ocupadas" in df.columns:
        df["personas_ocupadas"] = to_number(df["personas_ocupadas"])
    df["anio"] = 2022
    return df[[c for c in ["anio", "provincia", "canton", "sexo", "grupo_edad", "personas_ocupadas", "ciiu"] if c in df.columns]].drop_duplicates()
