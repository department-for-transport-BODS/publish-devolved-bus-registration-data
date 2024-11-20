import logging
import requests
from http import HTTPStatus
from os import getenv
from pydantic import ValidationError
from requests import HTTPError, RequestException, Timeout
from .aws import get_secret
from .logger import log
from .pydant_model import APIResponse
from .settings import (
    ENVIRONMENT,
    WECA_PARAM_C,
    WECA_PARAM_T,
    WECA_PARAM_R,
    WECA_API_URL,
)

WECA_AUTH_TOKEN = getenv("WECA_AUTH_TOKEN", None)

if ENVIRONMENT != "local":
    WECA_AUTH_TOKEN = get_secret(WECA_AUTH_TOKEN)["text_secret_data"]


class EmptyResponseException(Exception):
    pass


retry_exceptions = (RequestException, EmptyResponseException)


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
            log.exception(msg)
            raise

        except HTTPError as e:
            msg = f"HTTPError: {e}"
            log.exception(msg)
            raise

        if response.status_code == HTTPStatus.NO_CONTENT:
            log.warning(
                f"Empty Response, API return {HTTPStatus.NO_CONTENT}, "
                f"for params {params}"
            )
            return self.default_response()
        try:
            return APIResponse(**response.json())
        except ValidationError as exc:
            log.error("Validation error in WECA API response")
            log.error(f"Response JSON: {response.text}")
            log.error(f"Validation Error: {exc}")
        except ValueError as exc:
            log.error("Validation error in WECA API response")
            log.error(f"Response JSON: {response.text}")
            log.error(f"Validation Error: {exc}")
        return self.default_response()

    def default_response(self):
        """
        Create default return response for placeholder purpose
        """
        response = {"fields": [], "data": []}
        # print(response)
        return APIResponse(**response)

    def fetch_weca_services(self) -> APIResponse:
        """
        Fetch method for sending request to WECA
        Return Pydentic model response
        """
        response = self._make_request()
        return response
