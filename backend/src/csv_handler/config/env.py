# Env settings
from os import getenv


ENVIRONMENT = getenv("PROJECT_ENV", "local")
AWS_REGION = getenv("AWS_REGION", "Running locally")

