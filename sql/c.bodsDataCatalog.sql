CREATE TABLE IF NOT EXISTS bods_data_catalog (
    id SERIAL PRIMARY KEY,
    xml_service_code VARCHAR(255) UNIQUE,
    published_status VARCHAR(255),
    requires_attention BOOLEAN,
    timeliness_status VARCHAR(255)
);