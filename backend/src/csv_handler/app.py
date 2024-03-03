import csv
from fastapi import FastAPI, File, HTTPException, UploadFile, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO
from managers import CSVManager
from mangum import Mangum
from time import sleep
from utils.config import app,AWS_REGION,ENVIRONMENT 
from utils.logger import log
from auth.verifier import get_token_header



@app.get("/")
def read_root():
    return {
        "message": "FastAPI running on AWS Lambda and is executed in region "
        + AWS_REGION
        + ", using runtime environment "
        + ENVIRONMENT
    }

@app.get("/health")
def health_check():
    from utils.db import send_to_db

    send_to_db()
    return {"status": "ok"}

@app.get("/items")
def read_item():
    return {"item_id": 1}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    if ENVIRONMENT == "local":
        log.debug("Sleeping for 2 seconds to simulate file upload")
        sleep(2)
    # Decode the CSV data
    csv_str = contents.decode("utf-8")
    # Convert the CSV data into a dictionary
    csv_data = list(csv.DictReader(StringIO(csv_str)))
    csv_handler = CSVManager(csv_data)
    records_report = csv_handler.validation_and_insertion_steps()
    # Validate the CSV input data
    if records_report.get("invalid_records"):
        raise HTTPException(status_code=422, detail=records_report)
    return records_report

lambda_handler = Mangum(app, lifespan="off")
