import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

from .logger import log


class Registration(BaseModel):
    licence_number: str = Field(
        ..., min_length=1, json_schema_extra="PC7654321", alias="licenceNumber"
    )
    registration_number: str = Field(
        json_schema_extra="PD7654321/87654321", alias="registrationNumber"
    )
    route_number: str = Field(..., json_schema_extra="2", alias="routeNumber")
    route_description: str = Field(
        ...,
        json_schema_extra="City Center - Suburb - Main Street",
        alias="routeDescription",
    )
    variation_number: int = Field(..., json_schema_extra=1, alias="variationNumber")
    start_point: str = Field(..., json_schema_extra="City Center", alias="startPoint")
    finish_point: str = Field(..., json_schema_extra="Suburb", alias="finishPoint")
    via: str = Field(..., json_schema_extra="Main Street", alias="via")
    subsidised: str = Field(..., json_schema_extra="Fully", alias="subsidised")
    subsidy_detail: str = Field(
        ...,
        json_schema_extra="Transport for Local Authority (LA)",
        alias="subsidyDetail",
    )
    is_short_notice: bool = Field(..., json_schema_extra=False, alias="isShortNotice")
    received_date: str = Field(
        ..., json_schema_extra="01/01/2000", alias="receivedDate"
    )
    granted_date: str = Field(..., json_schema_extra="01/02/2000", alias="grantedDate")
    effective_date: str = Field(
        ..., json_schema_extra="01/03/2000", alias="effectiveDate"
    )
    end_date: str = Field(..., json_schema_extra="01/04/2000", alias="endDate")
    operator_name: str = Field(
        ..., json_schema_extra="Blue Sky Buses", alias="operatorName"
    )
    bus_service_type_id: str = Field(
        ..., json_schema_extra="Standard", alias="busServiceTypeId"
    )
    bus_service_type_description: str = Field(
        ..., json_schema_extra="Normal Stopping", alias="busServiceTypeDescription"
    )
    traffic_area_id: str = Field(..., json_schema_extra="C", alias="trafficAreaId")
    application_type: str = Field(..., json_schema_extra="New", alias="applicationType")
    publication_text: Optional[str] = Field(
        None,
        json_schema_extra="Revised timetable to improve reliability",
        alias="publicationText",
    )
    other_details: Optional[str] = Field(
        None, json_schema_extra="", alias="otherDetails"
    )

    @field_validator(
        "received_date", "granted_date", "effective_date", "end_date", mode="before"
    )
    def parse_date(cls, v):
        return datetime.strptime(v, "%m/%d/%Y").strftime("%Y-%m-%d")

    # @computed_field(return_type=int, repr=False)
    # @property
    # def service_code(cls):
    #     """Extract the service code from the registration number and save it as a field in the model"""
    #     v = cls.registration_number
    #     if isinstance(v, str):
    #         parts = v.split("/")
    #         if len(parts) == 2:
    #             return int(parts[1])

    @field_validator("registration_number")
    def validate_registration_number(cls, v):
        """Validate the registration number format"""
        if not re.match(r"[a-zA-Z0-9]+/[a-zA-Z0-9]+", v):
            raise ValueError("Invalid registration number format")
        return v


def csv_data_structure_check(csv_data: [dict]) -> dict:
    """This function checks the structure of the CSV data structure and returns a dictionary of valid and invalid records.
    It checks if a record adheres to the structure of the Registration model.
    Functionalities:
    1. Validate each record and deserialize it into a Python object.
    2. Invalid records are stored in a validation_errors list along with the record number.
    3. Valid records are stored in a pydantic_models list.
    4. Returns a dictionary of valid and invalid records.

    """
    # Convert the CSV data into a list of dictionaries
    # csv_data = list(csv.DictReader(file))
    valid_records = []
    validation_errors = {}

    for idx, data_dict in enumerate(csv_data):
        try:
            # Validate each record and deserialize it into a Python object.
            pydantic_model = Registration(**data_dict)
            valid_records.append(pydantic_model.model_dump(exclude=["serviceCode"]))
        except ValidationError as e:
            # Get json schema errors
            errors = e.errors()
            # Extract the field, message and type from the errors of a ValidationError object.
            modified_errors = extract_field_mgs_type_from_errors(errors)
            # validation_errors.append({"record_number": idx + 2,"errors": modified_errors})
            validation_errors.update({f"{idx + 2}": modified_errors})
        except Exception as e:
            log.error(f"Error: {e}")
    return {"invalid_records": validation_errors, "valid_records": valid_records}


def extract_field_mgs_type_from_errors(errors: [dict]) -> dict:
    """Extracts the field, message and type from the errors of a ValidationError object.

    Args:
        e (ValidationError): Contains the errors of a record.

    Returns:
        [dict]: A list of dictionaries containing the field, message and type of each error.
    """
    modified_errors = []
    for error in errors:
        # modified_error = {
        #                 "field": error.get("loc"),
        #                 "message": error.get("msg"),
        #                 "type": error.get("type")
        #         }
        if len(error.get("loc")) == 1:
            field_name = error.get("loc")[0]
            modified_errors.append({field_name: error.get("msg")})
        else:
            log.warning(
                f"Warning: Fields has more than one element. {error.get('loc')}"
            )

    return modified_errors
