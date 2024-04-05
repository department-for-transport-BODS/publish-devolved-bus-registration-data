from pydantic import ValidationError

from .logger import log
from .pydant_model import Registration


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
    
    if len(validation_errors) == 0:
        return {"invalid_records": [],"valid_records": valid_records}

    validation_description = "CSV data structure check"
    return {"invalid_records": [{"records" : validation_errors, "description": validation_description}], "valid_records": valid_records}


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
