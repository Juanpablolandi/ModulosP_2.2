import pandas as pd
from sqlalchemy import text
from etl.db import get_engine
from etl.utils.cleaning import build_time_dimension, clean_text


def append_df(df, table_name):
    if df is None or df.empty:
        return 0
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="append", index=False, method="multi", chunksize=1000)
    return len(df)


def upsert_dim_tiempo(fechas):
    df = build_time_dimension(fechas)
    if df.empty:
        return
    engine = get_engine()
    with engine.begin() as conn:
        for row in df.to_dict("records"):
            conn.execute(text("""
                INSERT INTO dim_tiempo (fecha, anio, mes, trimestre)
                VALUES (:fecha, :anio, :mes, :trimestre)
                ON CONFLICT (fecha) DO NOTHING;
            """), row)


def get_tiempo_map():
    engine = get_engine()
    return pd.read_sql("SELECT id_tiempo, fecha FROM dim_tiempo", engine)


def upsert_dim_geografia(df_geo):
    if df_geo is None or df_geo.empty:
        return
    df = df_geo.copy()
    for col in ["provincia", "canton"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
        else:
            df[col] = None
    for col in ["cod_provincia", "cod_canton"]:
        if col not in df.columns:
            df[col] = None
    df = df[["provincia", "cod_provincia", "canton", "cod_canton"]].dropna(subset=["provincia"]).drop_duplicates()
    engine = get_engine()
    with engine.begin() as conn:
        for row in df.to_dict("records"):
            conn.execute(text("""
                INSERT INTO dim_geografia (provincia, cod_provincia, canton, cod_canton)
                VALUES (:provincia, :cod_provincia, :canton, :cod_canton)
                ON CONFLICT (provincia, canton, cod_provincia, cod_canton) DO NOTHING;
            """), row)


def attach_id_tiempo(df, date_col="fecha"):
    if df.empty or date_col not in df.columns:
        return df
    upsert_dim_tiempo(df[date_col])
    tiempo = get_tiempo_map()
    tiempo["fecha"] = pd.to_datetime(tiempo["fecha"]).dt.date
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col]).dt.date
    return df.merge(tiempo, left_on=date_col, right_on="fecha", how="left", suffixes=("", "_dim"))


def attach_id_geo(df):
    if df.empty or "provincia" not in df.columns:
        return df
    geo_cols = [c for c in ["provincia", "cod_provincia", "canton", "cod_canton"] if c in df.columns]
    upsert_dim_geografia(df[geo_cols])
    engine = get_engine()
    geo = pd.read_sql("SELECT id_geo, provincia, cod_provincia, canton, cod_canton FROM dim_geografia", engine)
    for col in ["provincia", "canton"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
        geo[col] = geo[col].apply(clean_text)
    for col in ["cod_provincia", "cod_canton"]:
        if col not in df.columns:
            df[col] = None
    return df.merge(geo, on=["provincia", "cod_provincia", "canton", "cod_canton"], how="left")


def log_file(file_path, source_name, status, message=""):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO file_processing_log (file_name, file_path, source_name, status, message)
            VALUES (:file_name, :file_path, :source_name, :status, :message)
            ON CONFLICT (file_path) DO UPDATE
            SET processed_at = CURRENT_TIMESTAMP, status = EXCLUDED.status, message = EXCLUDED.message;
        """), {
            "file_name": file_path.name,
            "file_path": str(file_path.resolve()),
            "source_name": source_name,
            "status": status,
            "message": message,
        })


def already_processed(file_path):
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(text("SELECT 1 FROM file_processing_log WHERE file_path = :path AND status = 'OK'"), {"path": str(file_path.resolve())}).fetchone()
    return result is not None
