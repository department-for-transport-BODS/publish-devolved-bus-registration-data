CREATE TABLE IF NOT EXISTS pdbrd_stage(
    id SERIAL PRIMARY KEY,
    stage_id VARCHAR(255),
    stage_user INTEGER,
    stage_status VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT create_constraint_if_not_exists(
    'pdbrd_stage',
    'fk_pdbrd_user_id',
    'ALTER TABLE pdbrd_stage ADD CONSTRAINT fk_pdbrd_user_id FOREIGN KEY (stage_user) REFERENCES pdbrd_user(id);');
