from utils.csv_validator import csv_data_structure_check
from utils.db import send_to_db
from utils.validate import validate_licence_number_existence


class CSVManager:
    def __init__(self, csv_data: str):
        self.csv_data = csv_data

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
        validated_records = self._check_licence_number_existence(validated_records)
        self._send_to_db(validated_records)
        validated_records = self._remove_licence_details(validated_records)
        # Add the count of valid records to the validated_records dictionary
        validated_records["valid_records_count"] = len(
            validated_records["valid_records"]
        )
        del validated_records["valid_records"]
        return validated_records

    def _validate_csv_data(self):
        return csv_data_structure_check(self.csv_data)

    def _check_licence_number_existence(self, records):
        return validate_licence_number_existence(records)

    def _send_to_db(self, records):
        send_to_db(records)

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
