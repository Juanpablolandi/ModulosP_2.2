from etl.utils.io import read_table
from etl.utils.cleaning import normalize_columns, clean_text, to_number


def transform_ranking(path):
    df = normalize_columns(read_table(path))
    for col in ["ruc", "nombre", "situacion_legal", "provincia", "canton", "ciiu"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    for col in ["ingresos", "activos"]:
        if col in df.columns:
            df[col] = to_number(df[col])
    return df[[c for c in ["ruc", "nombre", "situacion_legal", "ingresos", "activos", "provincia", "canton", "ciiu"] if c in df.columns]].drop_duplicates()


def transform_directorio(path):
    df = normalize_columns(read_table(path))
    for col in ["ruc", "nombre", "situacion_legal", "provincia", "canton"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    return df[[c for c in ["ruc", "nombre", "situacion_legal", "provincia", "canton"] if c in df.columns]].drop_duplicates()
