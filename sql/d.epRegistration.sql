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

CREATE TABLE IF NOT EXISTS ep_registration (
    id SERIAL PRIMARY KEY,
    otc_licence_id INTEGER,
    route_number VARCHAR(255),
    route_description VARCHAR(255),
    variation_number INTEGER,
    start_point VARCHAR(255),
    finish_point VARCHAR(255),
    via VARCHAR(255),
    subsidised VARCHAR(10),
    subsidy_detail VARCHAR(255),
    is_short_notice BOOLEAN,
    received_date DATE,
    granted_date DATE,
    effective_date DATE,
    end_date DATE,
    otc_operator_id INTEGER,
    bus_service_type_id VARCHAR(255),
    bus_service_type_description VARCHAR(255),
    registration_number VARCHAR(255),
    traffic_area_id VARCHAR(255),
    application_type VARCHAR(255),
    publication_text VARCHAR(255),
    other_details VARCHAR(255),
    UNIQUE (otc_licence_id, registration_number, variation_number)
);

SELECT create_constraint_if_not_exists(
  'otc_licence',
  'fk_otc_licence',
  'ALTER TABLE ep_registration ADD CONSTRAINT fk_otc_licence FOREIGN KEY (otc_licence_id) REFERENCES otc_licence(id);');

SELECT create_constraint_if_not_exists(
  'otc_operator',
  'fk_otc_operator',
  'ALTER TABLE ep_registration ADD CONSTRAINT fk_otc_operator FOREIGN KEY (otc_operator_id) REFERENCES otc_operator(id);');