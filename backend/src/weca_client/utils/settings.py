from os import getenv
from dotenv import load_dotenv
from os import getenv
load_dotenv()


AWS_REGION = getenv("AWS_REGION", "Running locally")
PROJECT_ENV = getenv("PROJECT_ENV", "local")
API_TYPE_WECA = getenv("API_TYPE_WECA", "WECA") 
WECA_AUTH_TOKEN = getenv("WECA_AUTH_TOKEN")
WECA_PARAM_C = getenv("WECA_PARAM_C")
WECA_PARAM_T = getenv("WECA_PARAM_T")
WECA_PARAM_R = getenv("WECA_PARAM_R")
WECA_API_URL = getenv("WECA_API_URL")


# OTC API
OTC_CLIENT_API_URL = getenv("OTC_CLIENT_API_URL", "OTC_API_URL is not set")