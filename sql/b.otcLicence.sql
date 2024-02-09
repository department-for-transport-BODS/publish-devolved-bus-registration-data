CREATE TABLE IF NOT EXISTS otc_licence (
    id SERIAL PRIMARY KEY,
    licence_number VARCHAR(255),
    licence_status VARCHAR(255)
);