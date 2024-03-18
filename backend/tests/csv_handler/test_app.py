from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app
from os import remove
import uuid

client = TestClient(app)


def test_search_records():
    AutoMappingModels = MagicMock()
    AutoMappingModels.engine = MagicMock()
    params = {
        "licenseNumber": "ABC123",
        "registrationNumber": "123456",
        "operatorName": "Test Operator",
        "routeNumber": "123",
        "latestOnly": "Yes",
        "limit": "10",
        "strictMode": "Yes",
    }
    response = client.post(
        f"api/v1/search?licenseNumber={params['licenseNumber']}&registrationNumber={params['registrationNumber']}&operatorName={params['operatorName']}&routeNumber={params['routeNumber']}&latestOnly={params['latestOnly']}&limit={params['limit']}&strictMode={params['strictMode']}",
    )
    assert response.status_code == 422
    # assert response.json() == []


def test_search_records_validation_error():
    response = client.post(
        "api/v1/search",
        json={
            "licenseNumber": "ABC123",
            "registrationNumber": "123456",
            "operatorName": "Test Operator",
            "routeNumber": "123",
            "latestOnly": "Yes",
            "limit": "10",
            "strictMode": "InvalidValue",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": [],
                "msg": "Value error, At least one of the search parameters must be provided",
            }
        ]
    }


def test_create_upload_file_without_authentications():
    # Create a test file
    file_name = f"{str(uuid.uuid4())}.csv"
    test_file = open(file_name, "w")
    test_file.write("name,age\nJohn,25\nJane,30")
    test_file.close()

    # Send a POST request to the endpoint with the test file
    response = client.post("api/v1/upload-file/", files={"file": open(file_name, "rb")})

    # Assert that the response status code is 200
    assert response.status_code == 403

    # Assert that the response contains the expected filename
    assert response.json() == {"detail": "Not authenticated"}
    # Clean up the test file
    remove(file_name)


def test_create_upload_file_unsupported_format():
    # Create a test file
    file_name = f"{str(uuid.uuid4())}.csv"
    test_file = open(file_name, "w")
    test_file.write("name,age\nJohn,25\nJane,30")
    test_file.close()

    # Send a POST request to the endpoint with the test file
    response = client.post(
        "api/v1/upload-file/",
        files={"file": open(file_name, "rb")},
        headers={"Authorization": "Bearer localdev"},
    )

    # Assert that the response status code is 200
    assert response.status_code == 422

    # Assert that the response contains the expected filename
    assert response.json() == {
        "detail": {
            "invalid_records": {
                "2": [
                    {"licenceNumber": "Field required"},
                    {"registrationNumber": "Field required"},
                    {"routeNumber": "Field required"},
                    {"routeDescription": "Field required"},
                    {"variationNumber": "Field required"},
                    {"startPoint": "Field required"},
                    {"finishPoint": "Field required"},
                    {"via": "Field required"},
                    {"subsidised": "Field required"},
                    {"subsidyDetail": "Field required"},
                    {"isShortNotice": "Field required"},
                    {"receivedDate": "Field required"},
                    {"grantedDate": "Field required"},
                    {"effectiveDate": "Field required"},
                    {"endDate": "Field required"},
                    {"operatorName": "Field required"},
                    {"busServiceTypeId": "Field required"},
                    {"busServiceTypeDescription": "Field " "required"},
                    {"trafficAreaId": "Field required"},
                    {"applicationType": "Field required"},
                ],
                "3": [
                    {"licenceNumber": "Field required"},
                    {"registrationNumber": "Field required"},
                    {"routeNumber": "Field required"},
                    {"routeDescription": "Field required"},
                    {"variationNumber": "Field required"},
                    {"startPoint": "Field required"},
                    {"finishPoint": "Field required"},
                    {"via": "Field required"},
                    {"subsidised": "Field required"},
                    {"subsidyDetail": "Field required"},
                    {"isShortNotice": "Field required"},
                    {"receivedDate": "Field required"},
                    {"grantedDate": "Field required"},
                    {"effectiveDate": "Field required"},
                    {"endDate": "Field required"},
                    {"operatorName": "Field required"},
                    {"busServiceTypeId": "Field required"},
                    {"busServiceTypeDescription": "Field " "required"},
                    {"trafficAreaId": "Field required"},
                    {"applicationType": "Field required"},
                ],
            },
            "valid_records_count": 0,
        },
    }
    # Clean up the test file
    remove(file_name)


@patch(
    "app.CSVManager.validation_and_insertion_steps",
    return_value={"valid_records_count": 2, "invalid_records": None},
)
def test_create_upload_file(mock_validation_and_insertion_steps):
    # Create a test file
    file_name = f"{str(uuid.uuid4())}.csv"
    test_file = open(file_name, "w")
    test_file.write("name,age\nJohn,25\nJane,30")
    test_file.close()

    # Send a POST request to the endpoint with the test file
    response = client.post(
        "api/v1/upload-file/",
        files={"file": open(file_name, "rb")},
        headers={"Authorization": "Bearer localdev"},
    )

    # Assert that the response status code is 201
    assert response.status_code == 201

    # Assert that the response contains the expected records report
    assert response.json() == {"valid_records_count": 2, "invalid_records": None}

    # Clean up the test file
    remove(file_name)


def test_search_records_options():
    response = client.options("api/v1/search")
    assert response.status_code == 200
    assert response.json() == {
        "description": "This is the endpoint to search for records in the database.",
        "parameters": {
            "licenseNumber": "The license name to filter the records. (str)",
            "registrationNumber": "The registration number to filter the records. (str)",
            "operator": "The operator to filter the records. (str)",
            "routeNumber": "The route number to filter the records. (str)",
            "latestOnly": "Whether to retrieve only the latest records. (bool)",
            "limit": "The maximum number of records per page. (int)",
        },
        "responses": {
            "200": {
                "Results": "The results of the search",
                "TotalRecords": "The total number of records found",
            },
            "403": "Forbidden",
        },
    }
