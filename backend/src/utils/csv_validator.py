import re
from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Field, ValidationError, computed_field,
                      field_validator)

from .logger import log


class Registration(BaseModel):
    licenceNumber: str = Field(...,min_length=1,json_schema_extra="PC2021320")
    registrationNumber: str = Field(json_schema_extra="PD0001111/43010100")
    routeNumber: str = Field(..., json_schema_extra="1")
    routeDescription: str = Field(..., json_schema_extra="Wigan - Highfield Grange Circular")
    variationNumber: int = Field(..., json_schema_extra=1)
    startPoint: str = Field(..., json_schema_extra="Wigan")
    finishPoint: str = Field(..., json_schema_extra="Highfield Grange Circular")
    via: str = Field(..., json_schema_extra="")
    subsidised: bool = Field(..., json_schema_extra=True)
    subsidyDetail: str = Field(..., json_schema_extra="Transport for Greater Manchester (TFGM)")
    isShortNotice: bool = Field(..., json_schema_extra=False)
    receivedDate: str = Field(..., json_schema_extra="09/01/2023")
    grantedDate: str = Field(..., json_schema_extra="09/01/2023")
    effectiveDate: str = Field(..., json_schema_extra="9/24/2023")
    endDate: str= Field(..., json_schema_extra="8/31/2028")
    operatorId: str = Field(..., json_schema_extra="1028807")
    busServiceTypeId: str = Field(..., json_schema_extra="Standard")
    busServiceTypeDescription: str = Field(..., json_schema_extra="Normal Stopping")
    trafficAreaId: str = Field(..., json_schema_extra="C")
    applicationType: str = Field(..., json_schema_extra="New")
    publicationTest: Optional[str] = Field(None, json_schema_extra="Revised timetable to improve reliability")
    otherDetails: Optional[str] = Field(None, json_schema_extra="")

    @field_validator('receivedDate','grantedDate','effectiveDate','endDate', mode='before')
    def parse_date(cls, v):
        return datetime.strptime(v, '%m/%d/%Y').strftime('%Y-%m-%d')

    @computed_field(return_type=int, repr=False)
    @property
    def serviceCode(cls):
        """Extract the service code from the registration number and save it as a field in the model"""
        v = cls.registrationNumber
        if isinstance(v, str):
            parts = v.split('/')
            if len(parts) == 2:
                return int(parts[1])
    
    @field_validator('registrationNumber')
    def validate_registration_number(cls, v):
        """Validate the registration number format"""
        if not re.match(r'[a-zA-Z0-9]+/[a-zA-Z0-9]+', v):
            raise ValueError('Invalid registration number format')
        return v


def csv_data_structure_check(csv_data: [dict]) -> dict:
    """This function checks the structure of the CSV data structure and returns a dictionary of valid and invalid records.
    It checs if a records adheres to the structure of the Registration model.
    Functionalities:
    1. Validate each record and deserialize it into a Python object.
    2. Invalide records are stored in a validation_errors list along with the record number.
    3. Valid records are stored in a pydantic_models list.
    4. Returns a dictionary of valid and invalid records.

    """
    # Convert the CSV data into a list of dictionaries
    # csv_data = list(csv.DictReader(file))
    Valid_records = []
    validation_errors = []
    
    for idx, data_dict in enumerate(csv_data):
        try:
            # Validate each record and deserialize it into a Python object.
            pydantic_model = Registration(**data_dict)
            Valid_records.append(pydantic_model.model_dump(exclude=['serviceCode']))
        except ValidationError as e:
            # Get json schema errors
            errors  = e.errors()
            # Extract the field, message and type from the errors of a ValidationError object.
            modified_errors = extract_field_mgs_type_from_errors(errors)
            validation_errors.append({"recrod_number": idx + 2,"errors": modified_errors})
        except Exception as e:
            log.error(f"Error: {e}")
    return {"Invalid_records":validation_errors,"Valid_records":len(Valid_records)}

def extract_field_mgs_type_from_errors(errors: [dict]) -> [dict]:
    """Extracts the field, message and type from the errors of a ValidationError object.

    Args:
        e (ValidationError): Contains the errors of a record.

    Returns:
        [dict]: A list of dictionaries containing the field, message and type of each error.
    """
    modified_errors = []
    for error in errors:
        modified_error = {
                        "field": error.get("loc"),
                        "message": error.get("msg"),
                        "type": error.get("type")
                }
        modified_errors.append(modified_error)
    return modified_errors


