from pathlib import Path
import pandas as pd


def read_table(path, **kwargs):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path, engine="openpyxl", **kwargs)
    if suffix == ".csv":
        try:
            return pd.read_csv(path, **kwargs)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin-1", **kwargs)
    raise ValueError(f"Formato no soportado: {path.suffix}")
