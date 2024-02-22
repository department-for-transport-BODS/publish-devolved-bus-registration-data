import csv
from io import StringIO
from time import sleep

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from utils.config import (ALLOW_HEADER, ALLOW_METHODS, ALLOW_ORIGINS,
                          AWS_REGION, ENVIRONMENT)
from managers import CSVManager
from utils.logger import log

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADER,
)


@app.get("/")
def read_root():
    return {
        "message": "FastAPI running on AWS Lambda and is executed in region "
        + AWS_REGION
        + ", using runtime environment "
        + ENVIRONMENT
    }


@app.get("/items")
def read_item():
    return {"item_id": 1}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    if ENVIRONMENT == "localdev":
        log.debug("Sleeping for 2 seconds to simulate file upload")
        sleep(2)
    # Decode the CSV data
    csv_str = contents.decode("utf-8")
    # Convert the CSV data into a dictionary
    csv_data = list(csv.DictReader(StringIO(csv_str)))
    csv_handler = CSVManager(csv_data)
    records_report= csv_handler.validation_and_insertion_steps()
    # Validate the CSV input data
    if records_report.get("invalid_records"):
        raise HTTPException(status_code=422, detail=records_report)
    return records_report

@app.get("/health")
def health_check():
    from utils.db import send_to_db

    send_to_db()
    return {"status": "ok"}


lambda_handler = Mangum(app, lifespan="off")
