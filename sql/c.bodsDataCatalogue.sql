CREATE TABLE IF NOT EXISTS bods_data_catalogue (
    id SERIAL PRIMARY KEY,
    xml_service_code VARCHAR(255),
    variation_number INTEGER,
    service_type_description VARCHAR(255),
    published_status VARCHAR(255),
    requires_attention BOOLEAN,
    timeliness_status VARCHAR(255)
);