from pathlib import Path
from dotenv import load_dotenv
import os

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "macroentorno_ecuador"),
    "user": os.getenv("DB_USER", "macro_etl"),
    "password": os.getenv("DB_PASSWORD", "macro_etl_123"),
}

BRONZE_MANUAL_DIR = ROOT_DIR / os.getenv("BRONZE_MANUAL_DIR", "data/bronze/manual")
BRONZE_RPA_DIR = ROOT_DIR / os.getenv("BRONZE_RPA_DIR", "data/bronze/rpa")
LOG_DIR = ROOT_DIR / os.getenv("LOG_DIR", "logs")

BRONZE_MANUAL_DIR.mkdir(parents=True, exist_ok=True)
BRONZE_RPA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
