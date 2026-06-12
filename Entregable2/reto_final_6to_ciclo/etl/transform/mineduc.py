from etl.utils.io import read_table
from etl.utils.cleaning import normalize_columns, clean_text, to_number


def transform_amie(path):
    df = normalize_columns(read_table(path, sep=";"))
    df = df.rename(columns={"ao_lectivo": "anio_lectivo"})
    for col in ["amie", "nombre_institucion", "provincia", "canton", "nivel_educacion", "sostenimiento"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    if "total_estudiantes" in df.columns:
        df["total_estudiantes"] = to_number(df["total_estudiantes"])
    # Campo auxiliar para P3: bachillerato / último grado si existe una columna de grado/curso.
    
    if "nivel_educacion" in df.columns:
        df["es_bachillerato"] = df["nivel_educacion"].astype(str).str.contains("BACHILLER", na=False)
    else:
        df["es_bachillerato"] = False
    return df[[c for c in ["anio_lectivo", "amie", "nombre_institucion", "provincia", "canton", "nivel_educacion", "sostenimiento", "total_estudiantes", "es_bachillerato"] if c in df.columns]].drop_duplicates()
