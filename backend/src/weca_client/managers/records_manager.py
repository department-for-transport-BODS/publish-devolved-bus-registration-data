from utils.db import send_to_db
from utils.validate import validate_licence_number_existence
from copy import deepcopy
from utils.logger import log, console
from pydantic import ValidationError
from utils.pydant_model import Registration, AuthenticatedEntity


def extract_field_mgs_type_from_errors(errors: [dict]) -> dict:
    """Extracts the field, message and type from the errors of a ValidationError object.

    Args:
        e (ValidationError): Contains the errors of a record.

    Returns:
        [dict]: A list of dictionaries containing the field, message and type of each error.
    """
    modified_errors = []
    for error in errors:
        if error.get("loc") is None:
            log.warning("Warning: Field is None")
        elif len(error.get("loc")) == 1:
            field_name = error.get("loc")[0]
            modified_errors.append({field_name: error.get("msg")})
        else:
            log.warning(
                f"Warning: Fields has more than one element. {error.get('loc')}"
            )

    return modified_errors


def csv_data_structure_check(csv_data: [dict]) -> dict:
    """
    This function checks the structure of the CSV data structure and returns a dictionary of valid and invalid records.
    It checks if a record adheres to the structure of the Registration model.
    Functionalities:
    1. Validate each record and deserialize it into a Python object.
    2. Invalid records are stored in a validation_errors list along with the record number.
    3. Valid records are stored in a pydantic_models list.
    4. Returns a dictionary of valid and invalid records.
    """
    # Convert the CSV data into a list of dictionaries
    # csv_data = list(csv.DictReader(file))
    valid_records = {}
    validation_errors = {}

    for idx, data_dict in enumerate(csv_data):
        try:
            # Validate each record and deserialize it into a Python object.
            pydantic_model = Registration(**data_dict)
            valid_records.update(
                {f"{idx + 2}": pydantic_model}
            )  # .model_dump(exclude=["serviceCode"])
        except ValidationError as e:
            # Get json schema errors
            errors = e.errors()
            # Extract the field, message and type from the errors of a ValidationError object.
            modified_errors = extract_field_mgs_type_from_errors(errors)
            validation_errors.update({f"{idx + 2}": modified_errors})
        except Exception as e:
            log.error(f"Error: {e}")
    
    validation_description = "CSV data structure check"
    # if len(validation_errors) == 0:
    #     return {"invalid_records": [{"records" : validation_errors, "description": validation_description}],"valid_records": valid_records}
    return {"invalid_records": [{"records" : validation_errors, "description": validation_description}], "valid_records": valid_records}



class RecordsManager:
    def __init__(self, csv_data: str, authenticated_entity: AuthenticatedEntity = None, report_id: str = None):
        self.csv_data = csv_data
        self.group_name = authenticated_entity.group
        self.user_name = authenticated_entity.name
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
        self._send_to_db(validated_records, self.group_name, self.user_name)
        self._remove_licence_details(validated_records)
        # Add the count of valid records to the validated_records dictionary
        validated_records["valid_records_count"] = len(
            validated_records["valid_records"]
        )
        del validated_records["valid_records"]

        if validated_records["invalid_records"] == {}:
            del validated_records["invalid_records"]
        console.log(validated_records)
        # Send the report to the database
        # self._send_report_to_db(validated_records, self.user_name, self.group_name, self.report_id)


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
                    and record.route_number == records2.route_number
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

    def _send_to_db(self, records, group_name, user_name):
        send_to_db(records, group_name=group_name,user_name=user_name)

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

    # def _send_report_to_db(self, records_report, user_name, group_name , report_id):
    #     send_report_to_db(records_report, user_name, group_name, report_id)