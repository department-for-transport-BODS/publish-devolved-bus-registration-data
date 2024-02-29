from os import getenv

from dotenv import load_dotenv

load_dotenv()

# Env settings
ENVIRONMENT = getenv("PROJECT_ENV", "local")
AWS_REGION = getenv("AWS_REGION", "Running locally")

# Middleware settings
ALLOW_ORIGINS = ["*"]
ALLOW_METHODS = ["*"]
ALLOW_HEADER = ["*"]
