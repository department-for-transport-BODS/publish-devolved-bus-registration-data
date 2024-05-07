from os import getenv
from dotenv import load_dotenv
load_dotenv()


AWS_REGION = getenv("AWS_REGION", "Running locally")
PROJECT_ENV = getenv("PROJECT_ENV", "local")
WECA_AUTH_TOKEN = getenv("WECA_AUTH_TOKEN")
WECA_PARAM_C = getenv("WECA_PARAM_C")
WECA_PARAM_T = getenv("WECA_PARAM_T")
WECA_PARAM_R = getenv("WECA_PARAM_R")
WECA_API_URL = getenv("WECA_API_URL")


# OTC API
OTC_CLIENT_API_URL = getenv("OTC_CLIENT_API_URL", "OTC_API_URL is not set")


# User data
USER_TYPE = getenv("USER_TYPE")
USER_NAME = getenv("USER_NAME")
USER_GROUP = getenv("USER_GROUP")





# AuthenticatedEntity(type="user", name="weca_api", group="weca")