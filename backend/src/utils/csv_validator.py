from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import csv
from .logger import log
class Registration(BaseModel):
    licenceNumber: str = Field(example="PC2021320")
    registrationNumber: str = Field(example="PD0001111/43010100")
    routeNumber: int = Field(..., example=1)
    routeDescription: str = Field(..., example="Wigan - Highfield Grange Circular")
    variationNumber: int = Field(..., example=1)
    startPoint: str = Field(..., example="Wigan")
    finishPoint: str = Field(..., example="Highfield Grange Circular")
    via: str = Field(..., example="")
    subsidised: bool = Field(..., example=True)
    subsidyDetail: str = Field(..., example="Transport for Greater Manchester (TFGM)")
    isShortNotice: bool = Field(..., example=False)
    receivedDate: str = Field(..., example="09/01/2023")
    grantedDate: str = Field(..., example="09/01/2023")
    effectiveDate: str = Field(..., example="9/24/2023")
    endDate: str = Field(..., example="8/31/2028")
    operatorId: str = Field(..., example="1028807")
    busServiceTypeId: str = Field(..., example="Standard")
    busServiceTypeDescription: str = Field(..., example="Normal Stopping")
    trafficAreaId: str = Field(..., example="C")
    applicationType: str = Field(..., example="New")
    publicationTest: Optional[str] = Field(None, example="Revised timetable to improve reliability")
    otherDetails: Optional[str] = Field(None, example="")


def csv_data_structure_check(csv_data: [dict]) -> dict:
    '''This function checks the structure of the CSV data structure and returns a dictionary of valid and invalid records.
    It checs if a records adheres to the structure of the Registration model.
    Functionalities:
    1. Validate each record and deserialize it into a Python object.
    2. Invalide records are stored in a validation_errors list along with the record number.
    3. Valid records are stored in a pydantic_models list.
    4. Returns a dictionary of valid and invalid records.

    '''
    # Convert the CSV data into a list of dictionaries
    # csv_data = list(csv.DictReader(file))
    pydantic_models = []
    validation_errors = []
    
    for idx, data_dict in enumerate(csv_data):
        try:
            # Validate each record and deserialize it into a Python object.
            pydantic_model = Registration(**data_dict)
            pydantic_models.append(pydantic_model)
        except ValidationError as e:
            errors = e.errors()
            validation_errors.append({"recrod_number": idx + 1,"errors": errors})
    return {"Invalid_records":validation_errors,"Valid_records":pydantic_models}


def delete_url_field_and_rename_loc_to_field(validation_errors: [dict]) -> [dict]:
    '''This function has 2 functionalities.
    1. It removes the "url" field from the validation errors.
    2. It renames the "loc" key to "field".
    ''' 
    edited_errors = []
    from pprint import pprint
    for record in validation_errors:
        for error in record["errors"]:
            error["field"] = error.pop("loc")
            del error["url"]
        edited_errors.append(record)
    pprint(edited_errors,indent=4) 
    return edited_errors
