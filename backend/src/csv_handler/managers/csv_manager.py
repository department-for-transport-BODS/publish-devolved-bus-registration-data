import csv
from io import StringIO
from utils.csv_validator import csv_data_structure_check
from utils.db import send_to_db, send_report_to_db
from utils.validate import validate_licence_number_existence
from copy import deepcopy

class CSVManager:
    def __init__(self, csv_data: str, authenticated_entity_name: str = None, report_id: str = None):
        self.csv_data = csv_data
        self.group_name = authenticated_entity_name
        self.report_id = report_id

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
        self._send_to_db(validated_records, self.group_name)
        self._remove_licence_details(validated_records)
        # Add the count of valid records to the validated_records dictionary
        validated_records["valid_records_count"] = len(
            validated_records["valid_records"]
        )
        del validated_records["valid_records"]

        if validated_records["invalid_records"] == {}:
            del validated_records["invalid_records"]
        # Send the report to the database
        self._send_report_to_db(validated_records, self.group_name, self.report_id)


    def _validate_csv_data(self):
        return csv_data_structure_check(self.csv_data)

    def _check_duplicate_records(self, records):
        records_copy = deepcopy(records)
        duplicated_check_records = {}
        for idx, record in records_copy["valid_records"].items():
            duplicated_records = []
            for idx2, records2 in records_copy["valid_records"].items():
                if (
                    idx != idx2
                    and record.licence_number == records2.licence_number
                    and record.variation_number == records2.variation_number
                    and record.registration_number == records2.registration_number
                ):
                    duplicated_records.append(idx2)
            if duplicated_records:
                # if records["invalid_records"].get(idx):
                #     records["invalid_records"][idx].appand(
                #         {"CSV contains duplicated records": duplicated_records}
                #     )
                # else:
                # records["invalid_records"]["duplicated_records"][idx] = [
                duplicated_check_records[idx] = [
                    {
                        "": f"""Duplicate of record {(', ').join(duplicated_records)}"""
                    }
                ]
                try:
                    del records["valid_records"][idx]
                except KeyError:
                    pass
                for i in duplicated_records:
                    try:
                        del records["valid_records"][i]
                    except KeyError:
                        pass
        if len(duplicated_check_records) > 0:
            if records.get("invalid_records") is None:
                records["invalid_records"] = []
                validation_description = "CSV data structure check"
                records["invalid_records"].append({"records": duplicated_check_records, "description": validation_description})
            else:
                data_structure_invalid = records["invalid_records"][0]
                data_structure_invalid["records"].update(duplicated_check_records)
                records["invalid_records"][0] = data_structure_invalid
        

    def _check_licence_number_existence(self, records):
        validate_licence_number_existence(records)

    def _send_to_db(self, records, group_name):
        send_to_db(records, group_name,self.report_id)

    def _remove_licence_details(self, records):
        """Removing the licence details from validated records."""
        try:
            if "valid_records" in records:
                for idx, record in records["valid_records"].items():
                    if record and len(record) > 0:
                        records["valid_records"][idx] = record[0].model_dump(
                            exclude=["serviceCode"]
                        )
                    else:
                        print(f"Error: Invalid record at index {idx}")
            else:
                print("Error: 'valid_records' key not found in records")
        except Exception as e:
            print(f"Error: {e}")
        return records

    def _send_report_to_db(self, records_report, authenticated_entity_name, report_id):
        send_report_to_db(records_report, authenticated_entity_name, report_id)



def process_csv_file(content, authenticated_entity, report_id):
    # Decode the CSV data
    csv_str = None
    for encoding_types in ["utf-8-sig", "utf-8", "Latin-1", "ISO-8859-1"]:
        try:
            csv_str = content.decode(encoding_types)
            break
        except:
            pass
    if csv_str is None:
        raise Exception("File encoding not found")

    # Convert the CSV data into a dictionary
    csv_data = list(csv.DictReader(StringIO(csv_str)))
    csv_handler = CSVManager(csv_data, authenticated_entity.name, report_id)
    csv_handler.validation_and_insertion_steps()
    # Validate the CSV input data
    


