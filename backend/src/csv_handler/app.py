import csv
from fastapi import File, HTTPException, UploadFile, Depends, status
from io import StringIO
from managers import CSVManager
from mangum import Mangum
from time import sleep
from utils.logger import log
from auth.verifier import token_verifier
from central_config import app, PROJECT_ENV, AWS_REGION, api_v1_router


@api_v1_router.get("/health", dependencies=[Depends(token_verifier)])
def health_check():
    """ 
    This is a health check endpoint that is used to verify the status of the API.
    """
    return {"status": "ok"}


@api_v1_router.get("items")
def read_item():
    return {"item_id": 1}


@api_v1_router.post("uploadfile", dependencies=[Depends(token_verifier)], status_code=status.HTTP_201_CREATED)
async def create_upload_file(file: UploadFile = File(...)):
    """ This is the endpoint to upload a CSV file and process it.

    Args:
        file (UploadFile, optional): The CSV file to be uploaded

    Raises:
        HTTPException: 
            status_code: 422 if the CSV file contains invalid records
            status_code: 201 if all records in the CSV file is successfully processed and inserted into the database

    Returns:
        _type_: _description_
    """
    contents = await file.read()
    if PROJECT_ENV == "localdev":
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


@api_v1_router.get("/")
def read_root():
    return {
        "message": "FastAPI running on AWS Lambda and is executed in region "
        + AWS_REGION
        + ", using runtime environment "
        + PROJECT_ENV
    }


app.include_router(api_v1_router)
lambda_handler = Mangum(app, lifespan="off")
