from os import getenv
from dotenv import load_dotenv

load_dotenv()
# ENV
PROJECT_ENV = getenv("PROJECT_ENV", "local")

# LOGGING
LOGGER_LEVEL = getenv("LOG_LEVEL", "INFO")
LOGGER_MOD = getenv("LOGGER_MOD", "local")
# AWS env
AWS_REGION = getenv("AWS_REGION", "Running locally")
USERPOOL_ID = getenv("COGNITO_USERPOOL_ID", "COGNITO_USERPOOL_ID is not set")
APP_CLIENT_ID = getenv("COGNITO_APP_CLIENT_ID", "APP_CLIENT_ID is not set")
