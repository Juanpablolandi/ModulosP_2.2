import re
import pandas as pd
from unidecode import unidecode


def normalize_column_name(col):
    text = str(col).strip().lower()
    text = unidecode(text)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def normalize_columns(df):
    df = df.copy()
    df.columns = [normalize_column_name(c) for c in df.columns]
    return df


def clean_text(value):
    if pd.isna(value):
        return None
    text = unidecode(str(value)).strip().upper()
    text = re.sub(r"\s+", " ", text)
    return text


def to_number(series):
    return (
        series.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.replace(r"[^0-9\.-]", "", regex=True)
        .replace({"": None, "nan": None, "None": None})
        .pipe(pd.to_numeric, errors="coerce")
    )


def to_date(series):
    return pd.to_datetime(series, errors="coerce").dt.date


def build_time_dimension(fechas):
    values = pd.to_datetime(pd.Series(fechas).dropna().unique(), errors="coerce").dropna()
    df = pd.DataFrame({"fecha": values})
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["trimestre"] = df["fecha"].dt.quarter
    df["fecha"] = df["fecha"].dt.date
    return df.drop_duplicates("fecha")
