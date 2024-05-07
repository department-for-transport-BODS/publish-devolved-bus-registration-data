from os import getenv


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
USER_TYPE = getenv("user_type")
USER_NAME = getenv("user_name")
USER_GROUP = getenv("user_group")





# AuthenticatedEntity(type="user", name="weca_api", group="weca")