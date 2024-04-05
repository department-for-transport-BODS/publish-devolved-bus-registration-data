CREATE TABLE ep_report (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(255) NOT NULL,
    group_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    report JSONB
);

SELECT create_constraint_if_not_exists(
  'ep_group',
  'fk_ep_group',
  'ALTER TABLE ep_report ADD CONSTRAINT fk_ep_group FOREIGN KEY (group_id) REFERENCES ep_group(id);');