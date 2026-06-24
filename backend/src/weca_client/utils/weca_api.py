from os import getenv
import json

from pydantic import ValidationError
import boto3

from .logger import log
from .pydant_model import APIResponse


class WecaClient:
    def _make_request(self, **kwargs) -> APIResponse:
        """
        Send Request to WECA API Endpoint
        Response will be returned in the JSON format
        """

        s3_bucket = getenv("AWS_WECA_RAW_STORAGE_BUCKET_NAME")
        key = getenv(
            "WECA_S3_KEY_REGISTRATIONS", "raw/weca/weca_registrations_latest.json"
        )
        s3_client = boto3.client("s3")
        try:
            response_json = json.loads(
                s3_client.get_object(Bucket=s3_bucket, Key=key)["Body"]
                .read()
                .decode("utf-8")
            )
        except Exception as e:
            log.error(f"Error fetching WECA data from S3: {e}")
            return self.default_response()

        try:
            return APIResponse(**response_json)
        except ValidationError as exc:
            log.error("Validation error in WECA API response")
            log.error(f"Response JSON: {response_json}")
            log.error(f"Validation Error: {exc}")
        except ValueError as exc:
            log.error("Validation error in WECA API response")
            log.error(f"Response JSON: {response_json}")
            log.error(f"Validation Error: {exc}")
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
