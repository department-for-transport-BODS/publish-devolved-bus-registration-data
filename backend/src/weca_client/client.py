import logging
import requests
from http import HTTPStatus
from datetime import datetime, date
from typing import Optional, List
from requests import HTTPError, RequestException, Timeout

from pydantic import ValidationError

from pydantic import Field, field_validator
from pydantic import BaseModel
from constants import API_TYPE_WECA, WECA_AUTH_TOKEN, WECA_PARAM_C, WECA_PARAM_T, WECA_PARAM_R, WECA_API_URL
from logger import console

logger = logging.getLogger(__name__)


class EmptyResponseException(Exception):
    pass


retry_exceptions = (RequestException, EmptyResponseException)


class FieldModel(BaseModel):
    id: str
    name: str
    desc: str
    datatype: str


class DataModel(BaseModel):
    id: int
    registration_number: str = Field(alias="fullserialnumbe_trationrations")
    variation_number: str = Field(alias="fullserialnumbe_trationrations")
    licence: str = Field(alias="fullserialnumbe_trationrations")
    service_number: str = Field(alias="servicenumbers_icespt7a")
    start_point: str = Field(alias="startpoint_espt")
    finish_point: str = Field(alias="endpoint_sp")
    via: str = Field(alias="via_services_pt7atfu9e78z39yqc")
    effective_date: date = Field(alias="proposedstartda_rviceslvicespt")
    api_type: str = Field(default=API_TYPE_WECA)
    atco_code: Optional[str] = Field(alias="fullserialnumbe_trationrations")

    @field_validator("effective_date", mode="before")
    def parse_effective_date(cls, value):
        return datetime.strptime(value, "%d %b %Y")

    @field_validator("registration_number")
    def trim_registration_number(cls, value):
        # Split the registration number by slashes and take the first two parts
        parts = value.split("/")
        if len(parts) >= 2:
            return "/".join(parts[:2])
        else:
            return value

    @field_validator("variation_number")
    def trim_variation_number(cls, value):
        # Split the variation number by slashes and take the third part
        parts = value.split("/")
        if len(parts) == 3:
            return parts[2]
        else:
            return "0"

    @field_validator("licence")
    def extract_licence(cls, value):
        # Split the registration number by slashes and take the first parts
        parts = value.split("/")
        if len(parts) >= 1:
            return parts[0]
        else:
            return value

    @field_validator("atco_code",mode="before")
    def extract_atco_code(cls, value):
        # Extract the first three digits after the first slash of registration_number
        reg_number_parts = value.split("/")
        if len(reg_number_parts) > 1:
            if len(reg_number_parts[1]) >= 3:
                return reg_number_parts[1][:3]
            else:
                return reg_number_parts[1]
        else:
            return value


class APIResponse(BaseModel):
    fields: List[FieldModel]
    data: List[DataModel]


class WecaClient:
    def _make_request(self, timeout: int = 30, **kwargs) -> APIResponse:
        """
        Send Request to WECA API Endpoint
        Response will be returned in the JSON format
        """
        url = WECA_API_URL

        params = {
            "c": WECA_PARAM_C,
            "t": WECA_PARAM_T,
            "r": WECA_PARAM_R,
            "get_report_json": "true",
            "json_format": "json",
            **kwargs,
        }
        files = []
        headers = {"Authorization": WECA_AUTH_TOKEN}

        try:
            response = requests.post(
                url=url,
                headers=headers,
                params=params,
                files=files,
                timeout=timeout,
            )
            response.raise_for_status()
        except Timeout as e:
            msg = f"Timeout Error: {e}"
            logger.exception(msg)
            raise

        except HTTPError as e:
            msg = f"HTTPError: {e}"
            logger.exception(msg)
            raise

        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(
                f"Empty Response, API return {HTTPStatus.NO_CONTENT}, "
                f"for params {params}"
            )
            return self.default_response()
        try:
            console.log(response.json()["data"][0])
            return APIResponse(**response.json())
        except ValidationError as exc:
            logger.error("Validation error in WECA API response")
            logger.error(f"Response JSON: {response.text}")
            logger.error(f"Validation Error: {exc}")
        except ValueError as exc:
            logger.error("Validation error in WECA API response")
            logger.error(f"Response JSON: {response.text}")
            logger.error(f"Validation Error: {exc}")
        return self.default_response()

    def default_response(self):
        """
        Create default return response for placeholder purpose
        """
        response = {"fields": [], "data": []}
        return APIResponse(**response)

    def fetch_weca_services(self) -> APIResponse:
        """
        Fetch method for sending request to WECA
        Return Pydentic model response
        """
        response = self._make_request()
        return response



if __name__=="__main__":
    client = WecaClient()
    res = client.fetch_weca_services()
    console.log(res.data[0])