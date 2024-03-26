CREATE TABLE IF NOT EXISTS ep_group (
    id SERIAL PRIMARY KEY,
    local_auth VARCHAR(255),
    Unique(local_auth)
);
