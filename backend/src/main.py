import csv
import os
from io import StringIO

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from .utils.csv_validator import csv_data_structure_check
from .utils.logger import log

load_dotenv()
log.info(f"Running in regions: {os.getenv('AWS_REGION', 'Running locally')}")
log.info(f"Running in environment: {os.getenv('DB_HOST', 'Running locally')}")


app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": "FastAPI running on AWS Lambda and is executed in region "
        + os.getenv("AWS_REGION", "Running locally")
        + ", using runtime environment "
        + os.getenv("AWS_EXECUTION_ENV", "Running locally")
    }


@app.get("/items")
def read_item():
    return {"item_id": 1}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Decode the CSV data
    csv_str = contents.decode("utf-8")
    # Convert the CSV data into a dictionary
    csv_data = list(csv.DictReader(StringIO(csv_str)))
    validated_records =  csv_data_structure_check(csv_data)
    if validated_records.get('Invalid_records'):
        raise HTTPException(status_code=422, detail=validated_records)
    return validated_records

lambda_handler = Mangum(app, lifespan="off")
