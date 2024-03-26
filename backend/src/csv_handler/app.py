import csv
from fastapi import File, HTTPException, Request, UploadFile, Depends, status, Query
from io import StringIO
from pydantic import ValidationError
from managers import CSVManager
from mangum import Mangum
from utils.exceptions import LimitIsNotSet, LimitExceeded, GroupIsNotFound
from auth.verifier import get_current_group
from central_config import app, PROJECT_ENV, AWS_REGION, api_v1_router
from utils.db import DBManager
from utils.pydant_model import SearchQuery


@api_v1_router.post(
    "/upload-file",
    status_code=status.HTTP_201_CREATED,
)
async def create_upload_file(
    file: UploadFile = File(...), group_name: str = Depends(get_current_group)
):
    """This is the endpoint to upload a CSV file and process it.

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
    # Decode the CSV data
    csv_str = contents.decode("utf-8-sig")
    # Convert the CSV data into a dictionary
    csv_data = list(csv.DictReader(StringIO(csv_str)))
    csv_handler = CSVManager(csv_data, group_name)
    records_report = csv_handler.validation_and_insertion_steps()
    # Validate the CSV input data
    if records_report.get("invalid_records"):
        raise HTTPException(status_code=422, detail=records_report)
    return records_report


@api_v1_router.post("/search", status_code=status.HTTP_200_OK)
async def search_records(
    group_name: str = Depends(get_current_group),
    licenseNumber: str = Query(
        None,
        description="The license name to filter the records",
        pattern="^[a-zA-Z0-9]*$",
    ),
    registrationNumber: str = Query(
        None, description="The registration number to filter the records"
    ),
    operatorName: str = Query(None, description="The operator to filter the records"),
    routeNumber: str = Query(
        None, description="The route number to filter the records"
    ),
    latestOnly: str = Query(
        "Yes", description="Whether to retrieve only the latest records"
    ),
    limit: str = Query(None, description="The maximum number of records per page"),
    strictMode: str = Query(
        "No",
        description="Strict mode for search",
        examples=[
            "true",
            "false",
        ],
    ),
    page: str = Query(None, description="The page number to retrieve"),
    request: Request = None,
):
    """This is the endpoint to search for records in the database.

    Args:
        licenseNumber (str): The license name to filter the records
        registrationNumber (str): The registration number to filter the records
        operator (str): The operator to filter the records
        routeNumber (str): The route number to filter the records
        latestOnly (str): Whether to retrieve only the latest records
        limit (str): The maximum number of records per page
        strictMode (str): Strict mode for search

    Returns:
        _type_: _description_
    """
    try:
        search_query = SearchQuery(
            license_number=licenseNumber,
            registrationNumber=registrationNumber,
            operatorName=operatorName,
            routeNumber=routeNumber,
            latestOnly=latestOnly,
            limit=limit,
            strictMode=strictMode,
            page=page,
        )
        records = DBManager.get_records(group_name, **search_query.model_dump())

        # Get the host and path from the request
        host = request.headers.get("host")
        path = request.url.path

        next_page = DBManager.construct_next_page_url(search_query, host, path)

        res = {"Results": records}
        if next_page:
            res.update({"NextPage": next_page})
        return res
    except ValidationError as e:
        from utils.pydant_model import (
            extract_error_fields,
        )

        # errors = convert_errors(e, CUSTOM_MESSAGES)
        errors = extract_error_fields(e.errors())
        raise HTTPException(status_code=422, detail=errors)
    except GroupIsNotFound:
        raise HTTPException(status_code=403, detail={"message": "User is not found"})

    except LimitIsNotSet as e:
        raise HTTPException(status_code=422, detail=str(e))
    except LimitExceeded as e:
        raise HTTPException(status_code=422, detail=str(e))


def read_root():
    return {
        "message": "Welcome to the EP Licences registration API",
    }


@api_v1_router.options("/search")
async def search_records_options():
    """This is the endpoint to return the options for the search endpoint"""
    description = {
        "licenseNumber": "The license name to filter the records",
        "registrationNumber": "The registration number to filter the records",
        "operatorName": "The operator to filter the records",
        "routeNumber": "The route number to filter the records",
        "latestOnly": "Whether to retrieve only the latest records",
        "limit": "The maximum number of records per page",
        "strictMode": "Strict mode for search",
        "page": "The page number to retrieve",
    }


@api_v1_router.get("/view-registrations/status", status_code=status.HTTP_200_OK)
async def view_registrations(group_name: str = Depends(get_current_group)):
    """This is the endpoint to view all the records in the database"""
    print("token", group_name)
    try:
        records = DBManager.get_record_reuiqred_attention_percentage(group_name)
        return records
    except GroupIsNotFound as e:
        print("GroupIsNotFound", e)
        return []
    except Exception as e:
        print("Exception", e)
        raise HTTPException(status_code=400, detail={})


@api_v1_router.get("/all-records", status_code=status.HTTP_200_OK)
async def get_all_records(group_name: str = Depends(get_current_group)):
    """This is the endpoint to view all the records in the database"""
    records = DBManager.get_all_records(group_name)
    return records


app.include_router(api_v1_router)
lambda_handler = Mangum(app, lifespan="off")
