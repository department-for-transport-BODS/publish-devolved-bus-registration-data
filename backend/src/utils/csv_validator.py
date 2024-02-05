from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import csv
class Registration(BaseModel):
    licenceNumber: str = Field(example="PC2021320")
    registrationNumber: str = Field(example="PD0001111/43010100")
    routeNumber: int = Field(..., example="1")
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



# first_name,last_name,addresss
class person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=5)
    last_name: str = Field(..., min_length=1, max_length=20)
    address: str
    

def validate_csv(csv_data: [dict]):
    # Convert the CSV data into a list of dictionaries
    # csv_data = list(csv.DictReader(file))
    pydantic_models = []
    validation_errors = []
    
    for data_dict in csv_data:
        try:
            # Validate each record and deserialize it into a Python object.
            pydantic_model = Registration(**data_dict)
            pydantic_models.append(pydantic_model)
        except ValidationError as e:
            validation_errors.append(e.errors())
    if pydantic_models:
        print(len(pydantic_models))
        # send_registration_records_to_db(pydantic_models)
    if validation_errors:
        print(validation_errors)
        raise HTTPException(status_code=400, detail=[{"Invalid_records":len(validation_errors)},validation_errors])
    print(pydantic_models)
    return {"Message": "Data is valid."}
