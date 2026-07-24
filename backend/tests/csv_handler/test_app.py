from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app
from os import remove
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

@patch("app.process_csv_file", side_effect=PreviousProcessNotCompleted)
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

@patch("app.process_csv_file", side_effect=Exception("Unexpected error"))
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

@patch("app.process_csv_file")
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

@patch("utils.db.DBManager.get_records", return_value=[])
def test_search_records_options(mock_get_records):
    response = client.get("api/v1/search")
    assert response.status_code == 200
    assert response.json() == {"Results": []}
    