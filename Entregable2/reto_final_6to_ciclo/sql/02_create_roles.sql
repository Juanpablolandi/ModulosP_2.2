-- Control de usuarios solicitado para 6to ciclo.
-- Cambiar las contraseñas antes de entregar el proyecto final.
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'macro_etl') THEN
        CREATE ROLE macro_etl LOGIN PASSWORD 'macro_etl_123';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'macro_readonly') THEN
        CREATE ROLE macro_readonly LOGIN PASSWORD 'macro_readonly_123';
    END IF;
END $$;

GRANT CONNECT ON DATABASE macroentorno_ecuador TO macro_etl, macro_readonly;
