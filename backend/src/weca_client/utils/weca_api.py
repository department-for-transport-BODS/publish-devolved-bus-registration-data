import logging
import requests
from http import HTTPStatus
from requests import HTTPError, RequestException, Timeout
from pydantic import ValidationError
from .pydant_model import  APIResponse
from .settings import (
    WECA_AUTH_TOKEN,
    WECA_PARAM_C,
    WECA_PARAM_T,
    WECA_PARAM_R,
    WECA_API_URL,
)

logger = logging.getLogger(__name__)


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
        # print(response)
        return APIResponse(**response)

    def fetch_weca_services(self) -> APIResponse:
        """
        Fetch method for sending request to WECA
        Return Pydentic model response
        """
        response = self._make_request()
        return response


# if __name__ == "__main__":
#     client = WecaClient()
#     res = client.fetch_weca_services()