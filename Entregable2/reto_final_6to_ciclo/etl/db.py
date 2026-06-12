from sqlalchemy import create_engine, text
from etl.config import DB_CONFIG


def get_engine():
    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(url, future=True)


def execute_sql_file(path):
    engine = get_engine()
    sql = path.read_text(encoding="utf-8")
    with engine.begin() as conn:
        conn.execute(text(sql))


def refresh_gold_views():
    views = [
        "gold_pib_tendencia",
        "gold_empleo_tendencia",
        "gold_petroleo_30dias",
        "gold_empresas_provincia",
        "gold_bachilleres_vs_empresas",
        "gold_vab_sector_provincia",
        "gold_iee_coyuntura",
    ]
    engine = get_engine()
    with engine.begin() as conn:
        for view in views:
            conn.execute(text(f"REFRESH MATERIALIZED VIEW {view};"))
