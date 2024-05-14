import requests
from cachetools import TTLCache
from os import getenv
from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel, Field, AliasChoices
import logging
from utils.aws import get_secret
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from typing import List


class OTCAuthorizationTokenException(Exception):
    pass


class OTCLicenceNotFound(Exception):
    pass


class MalformedOTCAPIResponse(Exception):
    pass


ENVIRONMENT = getenv("PROJECT_ENV", "local")
MS_LOGIN_URL = getenv("MS_LOGIN_URL", None)
MS_SCOPE = getenv("MS_SCOPE", None)
MS_TENANT_ID = getenv("MS_TENANT_ID", None)
MS_CLIENT_ID = getenv("MS_CLIENT_ID", None)
MS_CLIENT_SECRET = getenv("MS_CLIENT_SECRET", None)
OTC_API_URL = getenv("OTC_API_URL", None)
OTC_API_KEY = getenv("OTC_API_KEY", None)

if ENVIRONMENT != "local":
    MS_CLIENT_SECRET = get_secret(MS_CLIENT_SECRET)
    OTC_API_KEY = get_secret(OTC_API_KEY)

API_RETURN_LIMIT = 100

logging.basicConfig(format="%(levelname)s,%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, getenv("LOG_LEVEL", "INFO")))


class OTCLicence(BaseModel):
    licence_number: str = Field(
        ..., validation_alias=AliasChoices("licenceNumber", "licence_number")
    )
    licence_status: str = Field(
        default=None,
        validation_alias=AliasChoices("licenceStatus", "licence_status"),
    )
    otc_licence_id: int = Field(
        ...,
        validation_alias=AliasChoices("licenceId", "otc_licence_id"),
    )


class Operator(BaseModel):
    operator_name: str = Field(
        ..., validation_alias=AliasChoices("operatorName", "operator_name")
    )
    otc_operator_id: int = Field(
        ...,
        validation_alias=AliasChoices("operatorId", "otc_operator_id"),
    )


class OTCAuthenticator:
    """
    Class responsible for providing Microsoft oauth2 Bearer token
    for sake of sending requests to the OTC API.
    OTC API requires 'Authorization' header to be added.
    {
        ...,
        "Authorization": <token>
    }
    """

    def __init__(self):
        logger.debug("Initialising authenticator and getting initial token")
        self.cache = TTLCache(maxsize=1, ttl=3600)
        self.get_token()

    @property
    def token(self) -> str:
        """
        Fetch bearer token from Cache (Redis) or send request to generate new token.
        """
        cache_hit = self.cache.get("otc-auth-bearer", None)
        if cache_hit is None:
            logger.debug("API Token cache has expired")
            return self.get_token()
        else:
            return cache_hit

    def get_token(self) -> str:
        """
        Fetches Authorization Bearer token from MS.
        Updates cache with newly fetched auth token.

        Token cache timeout is calculated using the data received in response.

        expiry_time - 5mins (to invalidate cache while the first token is still active)
        """
        logger.debug("Attempting to get API token from MS Endpoint")
        url = f"{MS_LOGIN_URL}/{MS_TENANT_ID}/oauth2/v2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "client_secret": MS_CLIENT_SECRET,
            "client_id": MS_CLIENT_ID,
            "scope": MS_SCOPE,
            "grant_type": "client_credentials",
        }
        response = None
        try:
            response = requests.post(url=url, headers=headers, data=body)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            msg = f"Couldn't fetch Authorization token. {err}"
            logger.error(msg)
            logger.error(f"with credentials {body}")
            if response:
                logger.error(f"with content {response.content}")
            raise OTCAuthorizationTokenException(msg)

        auth_response = response.json()

        token_cache_timeout = auth_response["expires_in"] - 60 * 5
        self.cache = TTLCache(maxsize=1, ttl=token_cache_timeout)
        self.cache["otc-auth-bearer"] = auth_response["access_token"]
        logger.debug(f"Token cache set with timeout {token_cache_timeout}")
        return auth_response["access_token"]


class OTCAPIClient:
    def __init__(self):
        self.otc_auth = OTCAuthenticator()

    def _request(self, timeout: int = 30, **kwargs) -> str:
        headers = {
            "x-api-key": OTC_API_KEY,
            "Authorization": f"{self.otc_auth.token}",
        }
        defaults = {"limit": API_RETURN_LIMIT, "page": 1}
        params = {**defaults, **kwargs}
        try:
            response = requests.get(
                url=OTC_API_URL,
                headers=headers,
                params=params,
                timeout=timeout,
            )
            response.raise_for_status()
        except requests.Timeout as e:
            msg = f"Timeout Error: {e}"
            logger.error(msg)
            raise

        except requests.HTTPError as e:
            msg = f"HTTPError: {e}"
            logger.error(msg)
            raise

        if response.status_code == HTTPStatus.NO_CONTENT:
            msg = f"Empty Response, API return {HTTPStatus.NO_CONTENT} for params {params}"
            logger.error(msg)
            raise OTCLicenceNotFound("Licence not found on OTC API")

        return response.json()

    def _get_licence(self, licence_number):
        logger.debug(f"Attempting to get licence {licence_number} from OTC")
        try:
            return licence_number, self._request(
                licenceNo=licence_number, limit=1, page=1, latestVariation="true"
            )
        except OTCLicenceNotFound:
            return licence_number, None
        except Exception as e:
            msg = f"Could not get license {licence_number}: {e}"
            logger.error(msg)
            raise

    def _parse_licence(self, licence_number, returned_licence):
        logger.debug(f"Attempting to parse licence {licence_number} received from OTC")
        bus_search_component = returned_licence.get("busSearch", None)
        try:
            if bus_search_component is None:
                raise MalformedOTCAPIResponse(
                    f"OTC API Response for licence {licence_number} was malformed: no busSearch component"
                )
            if len(bus_search_component) == 0:
                raise MalformedOTCAPIResponse(
                    f"OTC API Response for licence {licence_number} was malformed: busSearch component contains no records"
                )
        except Exception as e:
            msg = f"Could not get license {licence_number}: {e}"
            logger.error(msg)
            return None, None
        try:
            parsed_licence = OTCLicence(**bus_search_component[0])
            parsed_licence_dump = parsed_licence.model_dump()

        except Exception as e:
            msg = f"Could not get license detail for licence {licence_number}: {e}"
            logger.error(msg)
            parsed_licence_dump = None
        try:
            parsed_operator = Operator(**bus_search_component[0])
            parsed_operator_dump = parsed_operator.model_dump()
        except Exception as e:
            msg = f"Could not get operator detail for licence {licence_number}: {e}"
            logger.error(msg)
            parsed_operator_dump = None
        return parsed_licence_dump, parsed_operator_dump

    def get_licences(self, licence_numbers: list):
        logger.info(
            f"Attempting to get the following licenses from OTC: {', '.join(licence_numbers)}"
        )
        # Remove duplicates
        unique_licence_numbers = list(set(licence_numbers))

        # Get licences from OTC API in batches of 20
        with ThreadPoolExecutor(max_workers=20) as executor:
            returned_licences = list(
                executor.map(self._get_licence, unique_licence_numbers)
            )

        # Construct response
        response = {}
        response["licences"] = []
        for licence_number, returned_licence in returned_licences:
            per_licence_response = {}
            per_licence_response["licence_number"] = licence_number
            if returned_licence is None:
                per_licence_response["licence_details"] = None
                per_licence_response["operator_details"] = None
            else:
                licence_details, operator_details = self._parse_licence(
                    licence_number, returned_licence
                )
                per_licence_response["licence_details"] = licence_details
                per_licence_response["operator_details"] = operator_details
            response["licences"].append(per_licence_response)

        return response


app = FastAPI(
    docs_url="/api/v1/otc/docs",
    redoc_url="/api/v1/otc/redoc",
    openapi_url="/api/v1/otc/openapi.json",
)


@app.post("/api/v1/otc/licences")
async def query_licences(licences: List[str]):
    try:
        print(licences)
        client = OTCAPIClient()
        output = client.get_licences(licences)
        return output
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


lambda_handler = Mangum(app, lifespan="off")