CREATE OR REPLACE FUNCTION create_constraint_if_not_exists (
    t_name text, c_name text, constraint_sql text
) 
RETURNS VOID AS
$func$
BEGIN
    -- Look for our constraint
    IF EXISTS (
        SELECT constraint_name 
        FROM information_schema.constraint_column_usage 
        WHERE table_name = t_name AND constraint_name = c_name) THEN

        RAISE NOTICE 'constraint %s already exists, skipping', c_name;
    ELSE
        BEGIN
            EXECUTE constraint_sql;
        EXCEPTION
            WHEN others THEN
                RAISE NOTICE 'an error occurred: %s', SQLERRM;
        END;
    END IF;
END;
$func$
LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS ep_stage(
    id SERIAL PRIMARY KEY,
    stage_id VARCHAR(255),
    stage_user INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT create_constraint_if_not_exists(
    'ep_group_id',
    'fk_ep_group_id',
    'ALTER TABLE ep_stage ADD CONSTRAINT fk_ep_group_id FOREIGN KEY (stage_user) REFERENCES ep_group(id);');
