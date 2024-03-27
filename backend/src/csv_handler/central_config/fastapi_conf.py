# Middleware settings
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

ALLOW_ORIGINS = ["*"]
ALLOW_METHODS = ["*"]
ALLOW_HEADER = ["*"]

# Add prefix to fastapi
API_PREFIX = "/api/v1"


app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)
api_v1_router = APIRouter(prefix=API_PREFIX)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADER,
)
