from datetime import date, datetime
import re
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from os import getenv
class DBCreds(BaseModel):
    PG_HOST: str = Field(default_factory=lambda: getenv("POSTGRES_HOST", "localhost"))
    PG_PORT: str = Field(default_factory=lambda: getenv("POSTGRES_PORT", "5432"))
    PG_DB: str = Field(default_factory=lambda: getenv("POSTGRES_DB", "postgres"))
    PG_USER: str = Field(alias="username")
    PG_PASSWORD: str = Field(alias="password")


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
    end_date: date = Field(..., json_schema_extra="01/04/2000", alias="endDate")
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
        "route_description",
        "subsidy_detail",
        "other_details",
        "publication_text",
        "finish_point",
        "start_point",
        "via",
        "operator_name",
        "application_type",
        "bus_service_type_description",
        mode="before",
    )
    def validate_route_description(cls, v):
        # Add cutation marks to the route description
        if isinstance(v, str) and len(v) > 0:
            return v.strip()
        return v

    @field_validator(
        "received_date", "granted_date", "effective_date", "end_date", mode="before"
    )
    def parse_date(cls, v):
        return datetime.strptime(v, "%d/%m/%Y")


    @field_validator("registration_number")
    def validate_registration_number(cls, v):
        """Validate the registration number format"""
        if not re.match(r"[a-zA-Z0-9]+/[a-zA-Z0-9]+", v):
            raise ValueError("Invalid registration number format")
        return v


class LicenceDetails(BaseModel):
    licence_number: str
    licence_status: str
    otc_licence_id: int


class OperatorDetails(BaseModel):
    operator_name: str
    otc_operator_id: int


class LicenceRecord(BaseModel):
    licence_number: str
    licence_details: LicenceDetails | None
    operator_details: OperatorDetails | None


class AuthenticatedEntity(BaseModel):
    type: Literal["app", "local_auth", "read_only", "user"]
    name: str
    group: str = None