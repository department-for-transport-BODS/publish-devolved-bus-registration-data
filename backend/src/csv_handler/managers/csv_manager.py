import csv
from io import StringIO
from utils.csv_validator import csv_data_structure_check
from utils.db import (
    complete_stage_process,
    initiate_stage_process,
    send_to_db,
    send_report_to_db,
)
from utils.validate import validate_licence_number_existence
from copy import deepcopy
from utils.pydant_model import AuthenticatedEntity
from utils.aws import ClamAVClient, invoke_this_lambda_async
from central_config import PROJECT_ENV
from utils.logger import log


class CSVManager:
    def __init__(
        self,
        csv_data: str,
        authenticated_entity: AuthenticatedEntity = None,
        report_id: str = None,
        stage_id: str = None,
    ):
        self.csv_data = csv_data
        self.group_name = authenticated_entity.group
        self.user_name = authenticated_entity.name
        self.report_id = report_id
        self.stage_id = stage_id

    def validation_and_insertion_steps(self) -> dict:
        """This function performs the following steps:
        1. Validate the CSV data structure.
        2. Check if the licence numbers exist in the database.
        3. Send the validated records to the database.
        4. Remove the licence details from the validated records.
        5. Add the count of valid records to the validated_records dictionary.

        Returns:
             Record reports: A dictionary containing the valid and invalid records and the count of valid records.
        """
        validated_records = self._validate_csv_data()
        self._check_duplicate_records(validated_records)
        self._check_licence_number_existence(validated_records)
        self._send_to_db(
            validated_records, self.group_name, self.user_name, self.stage_id
        )
        self._remove_licence_details(validated_records)
        # Add the count of valid records to the validated_records dictionary
        validated_records["valid_records_count"] = len(
            validated_records["valid_records"]
        )
        del validated_records["valid_records"]

        if validated_records["invalid_records"] == {}:
            del validated_records["invalid_records"]

        # Log the invalid records to provide an audit trail of dropped/rejected records
        log.info(
            f"Invalid records for report_id={self.report_id}: {validated_records.get('invalid_records')}"
        )

        # Send the report to the database
        self._send_report_to_db(
            validated_records, self.user_name, self.group_name, self.report_id
        )

    def _validate_csv_data(self):
        return csv_data_structure_check(self.csv_data)

    def _check_duplicate_records(self, records):
        records_copy = deepcopy(records)
        duplicated_check_records = {}
        # record_id is the CSV row number, not an array index
        for record_id, record in records_copy["valid_records"].items():
            duplicated_records = []
            for other_record_id, records2 in records_copy["valid_records"].items():
                if (
                    record_id != other_record_id
                    and record.licence_number == records2.licence_number
                    and record.variation_number == records2.variation_number
                    and record.registration_number == records2.registration_number
                    and record.route_number == records2.route_number
                ):
                    duplicated_records.append(other_record_id)
            if duplicated_records:
                # if records["invalid_records"].get(idx):
                #     records["invalid_records"][idx].appand(
                #         {"CSV contains duplicated records": duplicated_records}
                #     )
                # else:
                # records["invalid_records"]["duplicated_records"][idx] = [
                duplicated_check_records[record_id] = [
                    {"": f"""Duplicate of record {(', ').join(duplicated_records)}"""}
                ]
                try:
                    del records["valid_records"][record_id]
                except KeyError:
                    pass
                for duplicate_record_id in duplicated_records:
                    try:
                        del records["valid_records"][duplicate_record_id]
                    except KeyError:
                        pass
        if len(duplicated_check_records) > 0:
            if records.get("invalid_records") is None:
                records["invalid_records"] = []
                validation_description = "CSV data structure check"
                records["invalid_records"].append(
                    {
                        "records": duplicated_check_records,
                        "description": validation_description,
                    }
                )
            else:
                data_structure_invalid = records["invalid_records"][0]
                data_structure_invalid["records"].update(duplicated_check_records)
                records["invalid_records"][0] = data_structure_invalid

    def _check_licence_number_existence(self, records):
        validate_licence_number_existence(records)

    def _send_to_db(self, records, group_name, user_name, staged_id):
        send_to_db(records, group_name, user_name, staged_id)

    def _remove_licence_details(self, records):
        """Removing the licence details from validated records."""
        try:
            if "valid_records" in records:
                # record_id is the CSV row number, not an array index
                for record_id, record in records["valid_records"].items():
                    if record and len(record) > 0:
                        records["valid_records"][record_id] = record[0].model_dump(
                            exclude=["serviceCode"]
                        )
                    else:
                        print(f"Error: Invalid record {record_id}")
            else:
                print("Error: 'valid_records' key not found in records")
        except Exception as e:
            print(f"Error: {e}")
        return records

    def _send_report_to_db(self, records_report, user_name, group_name, report_id):
        send_report_to_db(records_report, user_name, group_name, report_id)


CSV_JOB_EVENT_KEY = "csv_scan_job"


def start_csv_processing(content: bytes, authenticated_entity, report_id: str) -> None:
    """Stage the upload and hand the scan and validation off, so the request returns
    well inside API Gateway's 29s limit. Results are read via /stage and /get-report."""
    stage_id = initiate_stage_process(
        authenticated_entity.name, authenticated_entity.group, report_id
    )
    job = {
        "report_id": report_id,
        "stage_id": stage_id,
        "authenticated_entity": authenticated_entity.model_dump(),
    }
    clamav = None
    try:
        clamav = ClamAVClient(report_id)
        clamav.upload(content)
        if PROJECT_ENV == "local":
            process_csv_job(job)
        else:
            invoke_this_lambda_async({CSV_JOB_EVENT_KEY: job})
    except Exception as e:
        log.error(f"Could not start processing report_id={report_id}: {e}")
        if clamav is not None:
            try:
                clamav.delete()
            except Exception as cleanup_error:
                log.error(
                    f"Could not delete unprocessed file for report_id={report_id}: {cleanup_error}"
                )
        _report_failed_file(authenticated_entity, report_id, stage_id)


def process_csv_job(job: dict) -> None:
    authenticated_entity = AuthenticatedEntity(**job["authenticated_entity"])
    report_id, stage_id = job["report_id"], job["stage_id"]
    clamav = None
    try:
        clamav = ClamAVClient(report_id)
        if not clamav.wait_until_clean():
            _report_failed_file(authenticated_entity, report_id, stage_id)
            return
        csv_str = _decode(clamav.read())
        csv_data = list(csv.DictReader(StringIO(csv_str)))
        CSVManager(
            csv_data, authenticated_entity, report_id, stage_id
        ).validation_and_insertion_steps()
    except Exception as e:
        log.error(f"Processing failed for report_id={report_id}: {e}")
        _report_failed_file(authenticated_entity, report_id, stage_id)
    finally:
        if clamav is not None:
            try:
                clamav.delete()
            except Exception as e:
                log.error(f"Could not delete scanned file for report_id={report_id}: {e}")


def _decode(content: bytes) -> str:
    for encoding_types in ["utf-8-sig", "utf-8", "Latin-1", "ISO-8859-1"]:
        try:
            return content.decode(encoding_types)
        except UnicodeDecodeError:
            pass
    raise Exception("File encoding not found")


def _report_failed_file(authenticated_entity, report_id, stage_id) -> None:
    send_report_to_db(
        {"invalid_file": [{"description": "File is infected"}]},
        authenticated_entity.name,
        authenticated_entity.group,
        report_id,
    )
    complete_stage_process(stage_id)
