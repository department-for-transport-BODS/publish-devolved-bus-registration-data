# Middleware settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ALLOW_ORIGINS = ["*"]
ALLOW_METHODS = ["*"]
ALLOW_HEADER = ["*"]

# Add prefix to fastapi
API_PREFIX = "/api"


app = FastAPI(root_path=API_PREFIX)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADER,
)