from os import getenv


# ENV
ENVIRONMENT = getenv("PROJECT_ENV", "local")

# LOGGING
LOGGER_LEVEL = getenv("LOG_LEVEL", "INFO")
LOGGER_MOD = getenv("LOGGER_MOD", "local")

# AWS RELATED
AWS_REGION = getenv("AWS_REGION", "Running locally")
WECA_PARAM_C = getenv("WECA_PARAM_C")
WECA_PARAM_T = getenv("WECA_PARAM_T")
WECA_PARAM_R = getenv("WECA_PARAM_R")
WECA_API_URL = getenv("WECA_API_URL")

# OTC CLIENT API
OTC_CLIENT_API_URL = getenv("OTC_CLIENT_API_URL", "OTC_API_URL is not set")

# PROGRAMMATIC USER DATA
USER_TYPE = getenv("USER_TYPE", "user")
USER_NAME = getenv("USER_NAME", "weca_api")
USER_GROUP = getenv("USER_GROUP", "weca")