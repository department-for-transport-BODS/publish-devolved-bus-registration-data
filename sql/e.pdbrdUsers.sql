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