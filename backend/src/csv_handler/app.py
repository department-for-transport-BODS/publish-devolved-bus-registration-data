import csv
from typing import Annotated
from fastapi import File, HTTPException, Header, UploadFile, Depends, status, Query
from io import StringIO
from managers import CSVManager
from mangum import Mangum
from time import sleep
from utils.logger import log, console
from auth.verifier import token_verifier
from central_config import app, PROJECT_ENV, AWS_REGION, api_v1_router
from utils.db import DBManager

@api_v1_router.get("/health", dependencies=[Depends(token_verifier)])
def health_check():
    """ 
    This is a health check endpoint that is used to verify the status of the API.
    """
    return {"status": "ok"}


@api_v1_router.get("/items")
def read_item():
    return {"item_id": 1}


@api_v1_router.post("/uploadfile", dependencies=[Depends(token_verifier)], status_code=status.HTTP_201_CREATED)
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


# @api_v1_router.get("/search", dependencies=[Depends(token_verifier)])
# async def search_records(
#     license_name: str = Query(None),
#     registration: str = Query(None),
#     registering_organization: str = Query(None),
#     operator: str = Query(None),
#     route_number: str = Query(None),
#     page: int = Query(1, ge=1),
#     limit: int = Query(10, ge=1),
#     latest_only: bool = Query(False)
# ):
#     """ This is the endpoint to search for records in the database.

#     Args:
#         license_name (str): The license name to filter the records
#         registration (str): The registration to filter the records
#         registering_organization (str): The registering organization to filter the records
#         operator (str): The operator to filter the records
#         route_number (str): The route number to filter the records
#         page (int): The page number for pagination
#         limit (int): The maximum number of records per page
#         latest_only (bool): Whether to retrieve only the latest records

#     Returns:
#         _type_: _description_
#     """
#     # Perform the search based on the provided filters
#     # You can use a database query or any other method to retrieve the matching records
#     # Adjust the code below to fit your specific implementation
#     search_results = []
#     if latest_only:
#         # Retrieve only the latest records
#         search_results = get_latest_records()
#     else:
#         # Retrieve all records based on the provided filters
#         search_results = get_records_by_filters(
#             license_name=license_name,
#             registration=registration,
#             registering_organization=registering_organization,
#             operator=operator,
#             route_number=route_number
#         )

#     # Perform pagination
#     start_index = (page - 1) * limit
#     end_index = start_index + limit
#     paginated_results = search_results[start_index:end_index]

#     return {
#         "page": page,
#         "limit": limit,
#         "total_records": len(search_results),
#         "results": paginated_results
#     }



@api_v1_router.get("/search", dependencies=[Depends(token_verifier)])
async def search_records(user_agent: Annotated[str | None, Header()]):
    """ This is the endpoint to search for records in the database.

    Args:
        search_term (str): The search term to be used to search for records in the database

    Returns:
        _type_: _description_
    """
    DBManager.get_latest_records()
    return {"status": "ok"}
    # x = Annotated[str | None, Header()]
    # console.log(Header())
    # console.log("Searching for records with search term: ", user_agent)
    # return {"search_term": user_agent}

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
