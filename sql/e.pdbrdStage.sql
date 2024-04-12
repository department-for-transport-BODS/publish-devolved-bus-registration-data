CREATE OR REPLACE FUNCTION create_constraint_if_not_exists (
    t_name text, c_name text, constraint_sql text
) 
RETURNS VOID AS
$func$
BEGIN
    -- Look for our constraint
    IF EXISTS (
        SELECT con.conname
            FROM pg_catalog.pg_constraint con
                INNER JOIN pg_catalog.pg_class rel
                    ON rel.oid = con.conrelid
                INNER JOIN pg_catalog.pg_namespace nsp
                    ON nsp.oid = connamespace
            WHERE nsp.nspname = 'public'
                  AND rel.relname = t_name AND con.conname = c_name) THEN

        RAISE NOTICE 'constraint % already exists, skipping', c_name;
    ELSE
        BEGIN
            EXECUTE constraint_sql;
        EXCEPTION
            WHEN others THEN
                RAISE NOTICE 'an error occurred: %', SQLERRM;
        END;
    END IF;
END;
$func$
LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS pdbrd_stage(
    id SERIAL PRIMARY KEY,
    stage_id VARCHAR(255),
    stage_user INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT create_constraint_if_not_exists(
    'pdbrd_stage',
    'fk_pdbrd_group_id',
    'ALTER TABLE pdbrd_stage ADD CONSTRAINT fk_pdbrd_group_id FOREIGN KEY (stage_user) REFERENCES pdbrd_group(id);');
