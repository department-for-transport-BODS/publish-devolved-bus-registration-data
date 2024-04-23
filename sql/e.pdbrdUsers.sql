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

CREATE TABLE IF NOT EXISTS pdbrd_user (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    group_id INT,
    Unique(user_name)
);

SELECT create_constraint_if_not_exists(
    'pdbrd_user',
    'fk_pdbrd_group',
    'ALTER TABLE pdbrd_user ADD CONSTRAINT fk_pdbrd_group FOREIGN KEY (group_id) REFERENCES pdbrd_group(id) ON DELETE cascade;');