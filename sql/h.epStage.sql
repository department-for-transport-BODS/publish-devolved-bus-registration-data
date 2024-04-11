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
