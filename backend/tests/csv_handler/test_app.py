from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app, lambda_handler
from os import remove
import base64
import json
import os
from io import BytesIO
import uuid
from auth.verifier import operator
from utils.pydant_model import AuthenticatedEntity
from utils.exceptions import PreviousProcessNotCompleted
import pytest

client = TestClient(app)


@pytest.fixture
def app_dependency_override():
    app.dependency_overrides[operator] = lambda: AuthenticatedEntity(
        type="user", name="testuser", group="testgroup"
    )
    yield
    app.dependency_overrides = {}


@patch("utils.db.DBManager.get_records", return_value=[])
def test_search_records(app_dependency_override):
    params = {
        "licenseNumber": "ABC123",
        "registrationNumber": "123456",
        "operatorName": "Test Operator",
        "routeNumber": "123",
        "latestOnly": "Yes",
        "limit": "10",
        "strictMode": "Yes",
    }
    response = client.get(
        f"api/v1/search?licenseNumber={params['licenseNumber']}&registrationNumber={params['registrationNumber']}&operatorName={params['operatorName']}&routeNumber={params['routeNumber']}&latestOnly={params['latestOnly']}&limit={params['limit']}&strictMode={params['strictMode']}",
        headers={"Authorization": "Bearer localdev"},
    )
    assert response.status_code == 200
    assert response.json() == {"Results": []}


@patch("utils.db.DBManager.get_records", return_value=[])
def test_search_records_validation_error(app_dependency_override):
    response = client.get(
        "api/v1/search?latestOnly=InvalidValue",
        headers={"Authorization": "Bearer local"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["latestOnly"],
                "msg": "Value error, Invalid value for LatestOnly. Must be one of 'True', 'False', 'Yes', 'No'",
            }
        ]
    }


@pytest.fixture
def file_name():
    # Create a test file
    file_name = f"{str(uuid.uuid4())}.csv"
    test_file = open(file_name, "w")
    test_file.write("name,age\nJohn,25\nJane,30")
    test_file.close()
    yield file_name
    # Clean up the test file
    remove(file_name)


def test_create_upload_file_without_authentications(file_name):
    # Send a POST request to the endpoint with the test file
    response = client.post("api/v1/upload-file/", files={"file": open(file_name, "rb")})

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

@patch("app.start_csv_processing", side_effect=PreviousProcessNotCompleted)
def test_create_upload_file_previous_process_not_completed(
    mock_process, file_name, app_dependency_override
):
    """Test 422 is returned when a previous process is still running."""
    response = client.post(
        "api/v1/upload-file/",
        files={"file": open(file_name, "rb")},
        headers={"Authorization": "Bearer localdev"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": {"message": "Previous process is not completed yet"}}

@patch("app.start_csv_processing", side_effect=Exception("Unexpected error"))
def test_create_upload_file_generic_exception(
    mock_process, file_name, app_dependency_override
):
    """Test 400 is returned when an unexpected error occurs during processing."""
    response = client.post(
        "api/v1/upload-file/",
        files={"file": open(file_name, "rb")},
        headers={"Authorization": "Bearer localdev"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": {"message": "Encountered an error while processing the file"}}

@patch("app.start_csv_processing")
def test_create_upload_file(mock_process, file_name, app_dependency_override):
    response = client.post(
        "api/v1/upload-file/",
        files={"file": open(file_name, "rb")},
        headers={"Authorization": "Bearer localdev"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "File is being processed"
    assert "report_id" in response.json()
    mock_process.assert_called_once()


def api_gateway_upload_event(csv_bytes):
    boundary = "TESTBOUNDARY"
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="data.csv"\r\n'
        "Content-Type: text/csv\r\n\r\n"
    ).encode() + csv_bytes + f"\r\n--{boundary}--\r\n".encode()
    return {
        "resource": "/api/v1/{proxy+}",
        "path": "/api/v1/upload-file",
        "httpMethod": "POST",
        "headers": {
            "content-type": f"multipart/form-data; boundary={boundary}",
            "host": "uat.example",
        },
        "multiValueHeaders": {},
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "requestContext": {
            "resourcePath": "/api/v1/{proxy+}",
            "httpMethod": "POST",
            "path": "/uat/api/v1/upload-file",
            "stage": "uat",
            "identity": {"sourceIp": "127.0.0.1"},
        },
        "pathParameters": {"proxy": "upload-file"},
        "body": base64.b64encode(body).decode(),
        "isBase64Encoded": True,
    }


def av_tags(status=None):
    return {"TagSet": [] if status is None else [{"Key": "av-status", "Value": status}]}


@pytest.fixture
def deployed_upload(app_dependency_override):
    """Run the upload flow as deployed: S3, Lambda and the DB stubbed at their boundaries."""
    s3, lambda_client = MagicMock(), MagicMock()
    s3.get_object_tagging.return_value = av_tags()
    clients = {"s3": s3, "lambda": lambda_client}
    sleep = MagicMock()
    with patch.dict(
        os.environ, {"AWS_LAMBDA_FUNCTION_NAME": "uat-pdbrd-csv-handler-lambda"}
    ), patch(
        "utils.aws.boto3.client",
        side_effect=lambda *args, **kwargs: clients[kwargs.get("service_name") or args[0]],
    ), patch("utils.aws.sleep", sleep), patch(
        "managers.csv_manager.PROJECT_ENV", "uat"
    ), patch(
        "managers.csv_manager.initiate_stage_process", return_value=7
    ), patch("managers.csv_manager.send_report_to_db") as send_report, patch(
        "managers.csv_manager.complete_stage_process"
    ) as complete_stage, patch("managers.csv_manager.CSVManager") as csv_manager:
        yield MagicMock(
            s3=s3,
            lambda_client=lambda_client,
            sleep=sleep,
            send_report=send_report,
            complete_stage=complete_stage,
            csv_manager=csv_manager,
        )


def upload(csv_bytes=b"a,b\n1,2\n"):
    return lambda_handler(api_gateway_upload_event(csv_bytes), MagicMock())


def dispatched_job_event(deployed_upload):
    return json.loads(deployed_upload.lambda_client.invoke.call_args.kwargs["Payload"])


def test_upload_file_responds_before_the_virus_scan_finishes(deployed_upload):
    """API Gateway cuts requests off at 29s, so the upload must hand the scan off."""
    deployed_upload.sleep.side_effect = AssertionError(
        "upload request waited on the ClamAV scan"
    )

    response = upload()

    assert response["statusCode"] == 200
    assert json.loads(response["body"])["message"] == "File is being processed"
    deployed_upload.s3.put_object.assert_called_once()
    deployed_upload.s3.get_object_tagging.assert_not_called()
    deployed_upload.send_report.assert_not_called()
    deployed_upload.lambda_client.invoke.assert_called_once()
    assert deployed_upload.lambda_client.invoke.call_args.kwargs["InvocationType"] == "Event"


def test_async_invocation_validates_the_clean_upload(deployed_upload):
    upload(b"a,b\n1,2\n")
    deployed_upload.s3.get_object_tagging.side_effect = [av_tags(), av_tags("clean")]
    deployed_upload.s3.get_object.return_value = {"Body": BytesIO(b"a,b\n1,2\n")}

    lambda_handler(dispatched_job_event(deployed_upload), MagicMock())

    rows, entity, report_id, stage_id = deployed_upload.csv_manager.call_args.args
    assert rows == [{"a": "1", "b": "2"}]
    assert (entity.name, entity.group, stage_id) == ("testuser", "testgroup", 7)
    deployed_upload.csv_manager.return_value.validation_and_insertion_steps.assert_called_once()
    assert deployed_upload.s3.get_object_tagging.call_count == 2
    deployed_upload.s3.delete_object.assert_called_once()
    deployed_upload.send_report.assert_not_called()


def test_async_invocation_rejects_an_infected_upload(deployed_upload):
    response = upload()
    report_id = json.loads(response["body"])["report_id"]
    deployed_upload.s3.get_object_tagging.return_value = av_tags("infected")
    deployed_upload.s3.get_object.return_value = {"Body": BytesIO(b"a,b\n1,2\n")}

    lambda_handler(dispatched_job_event(deployed_upload), MagicMock())

    deployed_upload.csv_manager.assert_not_called()
    deployed_upload.send_report.assert_called_once_with(
        {"invalid_file": [{"description": "File is infected"}]},
        "testuser",
        "testgroup",
        report_id,
    )
    deployed_upload.complete_stage.assert_called_once_with(7)
    deployed_upload.s3.delete_object.assert_called_once()


def test_upload_that_cannot_be_handed_off_completes_its_stage(deployed_upload):
    """Otherwise the stage stays in_progress and every later upload gets a 422."""
    deployed_upload.lambda_client.invoke.side_effect = Exception("lambda endpoint unreachable")

    response = upload()

    assert response["statusCode"] == 200
    deployed_upload.send_report.assert_called_once()
    deployed_upload.complete_stage.assert_called_once_with(7)
    deployed_upload.s3.delete_object.assert_called_once()

@patch("utils.db.DBManager.get_records", return_value=[])
def test_search_records_options(mock_get_records):
    response = client.get("api/v1/search")
    assert response.status_code == 200
    assert response.json() == {"Results": []}
    