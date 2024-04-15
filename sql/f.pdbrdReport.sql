CREATE TABLE IF NOT EXISTS pdbrd_report (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(255) NOT NULL,
    group_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    report JSONB
);

SELECT create_constraint_if_not_exists(
  'pdbrd_report',
  'fk_pdbrd_group',
  'ALTER TABLE pdbrd_report ADD CONSTRAINT fk_pdbrd_group FOREIGN KEY (group_id) REFERENCES pdbrd_group(id);');