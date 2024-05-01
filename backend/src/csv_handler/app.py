from fastapi import (
    File,
    HTTPException,
    Request,
    UploadFile,
    Depends,
    status,
    Query,
    BackgroundTasks,
)
from pydantic import ValidationError
from managers import process_csv_file
from mangum import Mangum
from utils.exceptions import LimitIsNotSet, LimitExceeded, GroupIsNotFound
from auth.verifier import  operator, read_only_or_programmatic_access, operator_or_programmatic_access
from central_config import app, api_v1_router
from utils.db import DBManager
from utils.pydant_model import (
    AuthenticatedEntity,
    SearchQuery,
    StagedRecord,
    GroupedStagedRecords,
    Action,
)
from uuid import uuid4
from utils.logger import log


@api_v1_router.post(
    "/upload-file",
    status_code=status.HTTP_200_OK,
)
async def create_upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    authenticated_entity: AuthenticatedEntity = Depends(operator),
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
    # Generate a unique ID for the CSV file
    report_id = str(uuid4())
    try:
        content = await file.read()
        background_tasks.add_task(
            process_csv_file, content, authenticated_entity, report_id
        )
    except Exception as e:
        log.error(f"Error: {e}")
        raise HTTPException(
            status_code=400,
            detail={"message": "Encountered an error while processing the file"},
        )

    return {"message": "File is being proccessed", "report_id": report_id}


@api_v1_router.get("/get-report", status_code=status.HTTP_200_OK)
async def get_report(
    authenticated_entity: AuthenticatedEntity = Depends(operator),
    report_id: str = Query(..., description="The request ID for the report"),
):
    """This is the endpoint to get the report for the CSV file uploaded.

    Args:
        report_id (str): The request ID for the report

    Raises:
        HTTPException: status_code: 404 if the report is not found

    Returns:
        report (json) : json format of the report.
    """
    records_report = DBManager.get_report_then_delete_it_from_db(
        authenticated_entity, report_id
    )
    if not records_report:
        raise HTTPException(status_code=404, detail={"message": "Report not found"})
    return {"Report": records_report, "ReportStatus": "Completed"}


@api_v1_router.get("/get-staged-process", status_code=status.HTTP_200_OK)
async def get_staged_process(
    authenticated_entity: AuthenticatedEntity = Depends(operator),
):
    """This is the endpoint to get the staged records in the database.

    Args:
        authenticated_entity (AuthenticatedEntity): The authenticated entity

    Returns:
        _type_: _description_
    """
    processes = DBManager.get_staged_process(authenticated_entity)
    return {"processes": processes, "status": "Completed"}
    


@api_v1_router.get("/get-staged", status_code=status.HTTP_200_OK)
async def get_staged_records(
    authenticated_entity: AuthenticatedEntity = Depends(operator),
    stage_id: str = Query(..., description="The staged records ID"),
):
    """This is the endpoint to get the staged records in the database.

    Args:
        authenticated_entity (AuthenticatedEntity): The authenticated entity

    Returns:
        _type_: _description_
    """
    records = DBManager.get_staged_records(authenticated_entity, stage_id)
    staged_records = []
    for record in records:
        staged_records.append(StagedRecord(**record))
    grouped_records = {}

    for record in staged_records:
        if record.licence_number not in grouped_records:
            grouped_records[record.licence_number] = GroupedStagedRecords(
                licence_number=record.licence_number,
                operator_name=record.operator_name,
                registration_numbers=[],
            )
        grouped_records[record.licence_number].registration_numbers.append(
            record.registration_number
        )
    values = list(grouped_records.values())
    return {"records": values, "status": "Completed"}


@api_v1_router.post("/staged-records/{action}", status_code=status.HTTP_200_OK)
def get_staged_records_action(
    action: str,
    authenticated_entity: AuthenticatedEntity = Depends(operator),
    stage_id: str = Query(
        ..., description="The staged records ID", pattern="^[a-zA-Z0-9\-]*$"
    ),
):
    """This is the endpoint to get the staged records in the database.

    Args:
        authenticated_entity (AuthenticatedEntity): The authenticated entity

    Returns:
        _type_: _description_
    """
    try:
        action = Action(action=action)

    except ValidationError as e:
        return {
            "message": "Invalid action, action should be either 'commit' or 'discard'"
        }
    try:
        result = None
        # Commit the staged records
        if action.action == "commit":
            result = DBManager.commit_staged_records(authenticated_entity, stage_id)
            if result:
                return {"message": "Staged records committed successfully"}
        # Discard the staged records
        if action.action == "discard":
            result = DBManager.commit_staged_records(
                authenticated_entity, stage_id, commit=False
            )
            if result:
                return {"message": "Staged records discarded successfully"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Staged records not found"},
        )
    except Exception as e:
        log.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Encountered an error while processing the request"},
        )


@api_v1_router.get("/search", status_code=status.HTTP_200_OK)
async def search_records(
    authenticated_entity: AuthenticatedEntity = Depends(read_only_or_programmatic_access),
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
        records = DBManager.get_records(
            authenticated_entity, **search_query.model_dump()
        )

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
        raise HTTPException(status_code=401, detail={"message": "Not authenticated"})
    except LimitIsNotSet as e:
        raise HTTPException(status_code=422, detail=str(e))
    except LimitExceeded as e:
        raise HTTPException(status_code=422, detail=str(e))


def read_root():
    return {
        "message": "Welcome to the PDBRD registration API",
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
async def view_registrations(authenticated_entity: str = Depends(operator)):
    """This is the endpoint to view all the records in the database"""
    try:
        records = DBManager.get_record_required_attention_percentage(
            authenticated_entity
        )
        return records
    except GroupIsNotFound as e:
        print("GroupIsNotFound", e)
        return []
    except Exception as e:
        print("Exception", e)
        raise HTTPException(status_code=400, detail={})


@api_v1_router.get("/all-records", status_code=status.HTTP_200_OK)
def get_all_records(
    authenticated_entity: str = Depends(operator_or_programmatic_access),
    latestOnly: str = Query(
        "No", description="Whether to retrieve only the latest records"
    ),
    activeOnly: str = Query(
        "No", description="Whether to retrieve only the active records"
    ),
):
    """This is the endpoint to view all the records in the database"""
    
    if latestOnly.lower() in ["yes", "true"]:
        user_choice_latest_only = True
    elif latestOnly.lower() in ["no", "false"]:
        user_choice_latest_only = False
    else:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Invalid value for latestOnly, it should be either 'Yes','No', 'True' or 'False'"
            },
        )
    if activeOnly.lower() in ["yes", "true"]:
        user_choice_active_only = True
    
    elif activeOnly.lower() in ["no", "false"]:
        user_choice_active_only = False
    else:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Invalid value for activeOnly, it should be either 'Yes','No', 'True' or 'False'"
            },
        )
    try:
        records = DBManager.get_all_records(
            authenticated_entity, latest_only=user_choice_latest_only, active_only=user_choice_active_only
        )
        return records
    except Exception as e:
        log.error(f"Error: {e}")
        raise HTTPException(status_code=422, detail={"message": "Error occurred while fetching records"})


app.include_router(api_v1_router)
lambda_handler = Mangum(app, lifespan="off")
