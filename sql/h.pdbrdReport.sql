CREATE TABLE IF NOT EXISTS pdbrd_report (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    report JSONB
);

SELECT create_constraint_if_not_exists(
  'pdbrd_report',
  'fk_pdbrd_user',
  'ALTER TABLE pdbrd_report ADD CONSTRAINT fk_pdbrd_user FOREIGN KEY (user_id) REFERENCES pdbrd_user(id);');