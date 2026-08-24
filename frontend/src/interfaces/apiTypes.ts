export interface InvalidRecord {
  records?: Record<string, unknown>;
}

export interface ReportData {
  invalid_file?: string | null;
  invalid_records: InvalidRecord[];
}

export interface StagedRecordsData {
  stage_id: string;
  records?: unknown[];
}

export interface Stage {
  created_at: string;
  stage_id: string;
}

export interface StageProcessesResponse {
  processes?: Stage[];
}

export interface PreValidationRecord {
  licence_number: string;
  operator_name: string;
  registration_numbers: string[];
}

