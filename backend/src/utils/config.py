from os import getenv

from dotenv import load_dotenv

load_dotenv()

# Env settings
ENVIRONMENT = getenv("PROJECT_ENV", "localdev")
AWS_REGION = getenv("AWS_REGION", "localdev")

# Middleware settings
ALLOW_ORIGINS = ["*"]
ALLOW_METHODS = ["*"]
ALLOW_HEADER = ["*"]
