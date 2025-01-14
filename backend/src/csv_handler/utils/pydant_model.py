import re
from datetime import datetime, date
from typing import Any, Dict, Literal, List, Optional
from os import getenv
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import ValidationError
from pydantic_core import ErrorDetails
from utils.constants import ACCEPTED_APPLICATION_TYPES


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
    received_date: date = Field(
        ..., json_schema_extra="01/01/2000", alias="receivedDate"
    )
    granted_date: date = Field(..., json_schema_extra="01/02/2000", alias="grantedDate")
    effective_date: date = Field(
        ..., json_schema_extra="01/03/2000", alias="effectiveDate"
    )
    end_date: Optional[date] = Field(
        None, json_schema_extra="01/04/2000", alias="endDate"
    )

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
    traffic_area_id: str = Field(
        default="WECA", json_schema_extra="C", alias="trafficAreaId"
    )
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
        "route_description",
        "route_number",
        "subsidy_detail",
        "other_details",
        "publication_text",
        "finish_point",
        "start_point",
        "via",
        "operator_name",
        "bus_service_type_description",
        mode="before",
    )
    def validate_route_description(cls, v):
        # Add cutation marks to the route description
        if isinstance(v, str) and len(v) > 0:
            return v.strip()
        return v

    @field_validator("application_type")
    def validate_application_type(cls, v):
        service_type = v.capitalize().strip()
        if service_type not in ACCEPTED_APPLICATION_TYPES:
            raise ValueError("Invalid application type")
        return service_type

    @field_validator("received_date", "granted_date", "effective_date", mode="before")
    def parse_date(cls, v):
        return datetime.strptime(v, "%d/%m/%Y")
    
    @field_validator("end_date", mode="before")
    def parse_end_date(cls, v):
        if v != "":
            return datetime.strptime(v, "%d/%m/%Y")
        return None

    @field_validator("registration_number")
    def validate_registration_number(cls, v):
        """Validate the registration number format"""
        if not re.match(r"[a-zA-Z0-9]+/[a-zA-Z0-9]+", v):
            raise ValueError("Invalid registration number format")
        return v

    @field_validator("route_number", mode="before")
    def validate_route_number(cls, v):
        # Prevent route number to have _ - / . , characters
        print("Route number")
        print(v)
        if v is not None:
            if re.search(r"[_\-/.,]", v):
                raise ValueError("invalid characters found in route number, please avoid using any of (_ - / . ,")
            return v




class LicenceDetails(BaseModel):
    licence_number: str
    licence_status: str


class OperatorDetails(BaseModel):
    operator_name: str


class LicenceRecord(BaseModel):
    licence_number: str
    licence_details: LicenceDetails | None
    operator_details: OperatorDetails | None


class DBCreds(BaseModel):
    host: str = Field(default_factory=lambda: getenv("POSTGRES_HOST", "localhost"))
    port: str = Field(default_factory=lambda: getenv("POSTGRES_PORT", "5432"))
    dbname: str = Field(default_factory=lambda: getenv("POSTGRES_DB", "postgres"))
    user: str = Field(default_factory=lambda: getenv("POSTGRES_USER", "postgres"))
    password: str = Field(alias="password")
    optargs: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"

    def __init__(self, **data):
        super().__init__(**data)
        self.optargs = {
            key: value for key, value in data.items() if key not in self.__fields__
        }


class InvalidLatestOnly(Exception):
    def __init__(self, message: str, value):
        self.message = message
        super().__init__(self.message, value)


class CustomValidationError(Exception):
    def json(self, *, indent: Optional[int] = None, **kwargs) -> str:
        errors = []
        for error in self.errors():
            error_dict = error["exc"].dict()
            error_dict.pop("ctx", None)  # Remove the 'ctx' key
            errors.append(error_dict)
        return self._json(errors, indent=indent, **kwargs)


CUSTOM_MESSAGES = {
    "int_parsing": "This is not an integer! 🤦",
    "url_scheme": "Hey, use the right URL scheme! I wanted {expected_schemes}.",
}


def convert_errors(
    e: ValidationError, custom_messages: Dict[str, str]
) -> List[ErrorDetails]:
    new_errors: List[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error["type"])
        if custom_message:
            ctx = error.get("ctx")
            error["msg"] = custom_message.format(**ctx) if ctx else custom_message
        new_errors.append(error)
    return new_errors


class SearchQuery(BaseModel):
    license_number: Optional[str] = (
        Field(default=None, alias="licenseNumber", pattern=r"^[a-zA-Z0-9]+$"),
    )
    registration_number: Optional[str] = Field(
        default=None, alias="registrationNumber", pattern=r"^[a-zA-Z0-9//]+$"
    )

    operator_name: Optional[str] = Field(
        default=None, alias="operatorName", pattern=r"^[a-zA-Z0-9\s\']+$"
    )
    route_number: Optional[str] = Field(default=None, alias="routeNumber")
    exclude_variations: bool = Field(alias="latestOnly", default=False)
    limit: Optional[int] = Field(default=10)
    strict_mode: Optional[bool] = Field(
        default=False, alias="strictMode", json_schema_extra="false"
    )
    page: Optional[int] = Field(default=None)
    active_only: Optional[bool] = Field(default=False, alias="activeOnly")

    @field_validator("exclude_variations", "active_only", "strict_mode", mode="before")
    def validate_latest_only(cls, v):
        if v is None:
            return True
        elif isinstance(v, str):
            v = v.lower()
            if v in ["true", "yes"]:
                return True
            elif v in ["false", "no"]:
                return False
        raise ValueError(
            "Invalid value for LatestOnly. Must be one of 'True', 'False', 'Yes', 'No'"
        )

class Error(BaseModel):
    type: str
    loc: tuple
    msg: str


class ErrorResponse(BaseModel):
    errors: List[Error]


def extract_error_fields(error_obj: List[dict], model_dump=True) -> ErrorResponse:
    errors = []
    for error in error_obj:
        error_fields = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": error.get("msg"),
        }
        errors.append(Error(**error_fields))

    if model_dump:
        return [error.model_dump() for error in errors]

    return errors


class AuthenticatedEntity(BaseModel):
    type: Literal["app", "local_auth", "read_only", "user"]
    name: str
    group: str = None


class StagedRecord(BaseModel):
    registration_number: str
    licence_number: str
    operator_name: str


class GroupedStagedRecords(BaseModel):
    licence_number: str
    operator_name: str
    registration_numbers: List[str]


class Action(BaseModel):
    action: Literal["commit", "discard"]


class StageEntity(BaseModel):
    type: Literal["record", "process"]
