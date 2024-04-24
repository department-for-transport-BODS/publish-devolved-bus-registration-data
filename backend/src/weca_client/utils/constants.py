from dotenv import load_dotenv
from os import getenv
load_dotenv()


API_TYPE_WECA = getenv("API_TYPE_WECA", "WECA") 
WECA_AUTH_TOKEN = getenv("WECA_AUTH_TOKEN")
WECA_PARAM_C = getenv("WECA_PARAM_C")
WECA_PARAM_T = getenv("WECA_PARAM_T")
WECA_PARAM_R = getenv("WECA_PARAM_R")
WECA_API_URL = getenv("WECA_API_URL")
