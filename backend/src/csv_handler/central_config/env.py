from os import getenv
from dotenv import load_dotenv

load_dotenv()
# ENV
PROJECT_ENV = getenv("PROJECT_ENV", "local")

# AWS env
AWS_REGION = getenv("AWS_REGION", "Running locally")
USERPOOL_ID = getenv("USERPOOL_ID", "USERPOOL_ID is not set")
APP_CLIENT_ID = getenv("APP_CLIENT_ID", "APP_CLIENT_ID is not set")
