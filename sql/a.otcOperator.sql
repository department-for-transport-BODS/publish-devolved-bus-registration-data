CREATE TABLE IF NOT EXISTS otc_operator (
    id SERIAL PRIMARY KEY,
    operator_name VARCHAR(255),
    operator_id VARCHAR(255) UNIQUE
);