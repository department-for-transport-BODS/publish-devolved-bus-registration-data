from pydantic import ValidationError

from utils.csv_validator import (Registration,
                                 extract_field_mgs_type_from_errors)


def test_extract_field_mgs_type_from_errors():
    # Create a ValidationError object with sample errors
    errors = [
        {
            "loc": ["first_name"],
            "msg": "Field required",
            "type": "missing",
            "ctx": {"limit_value": 1},
            "url": "dummy url",
        },
        {"msg": "Field required", "type": "missing"},
        {"loc": ["address"], "type": "missing"},
    ]
    # validation_error = ValidationError(errors)

    # Call the function and get the result
    result = extract_field_mgs_type_from_errors(errors)

    # Assert that the result matches the expected output
    expected_result = [{'first_name': 'Field required'}, {'address': None}]
    assert result == expected_result


def test_registration_model():
    # Create a valid registration object
    registration_data = {
        "licenceNumber": "PC7654321",
        "registrationNumber": "PD7654321/87654321",
        "routeNumber": "2",
        "routeDescription": "City Center - Suburb - Main Street",
        "variationNumber": 2,
        "startPoint": "City Center",
        "finishPoint": "Suburb",
        "via": "Main Street",
        "subsidised": "Fully",
        "subsidyDetail": "Transport for Local Authority (LA)",
        "isShortNotice": False,
        "receivedDate": "01/02/2000",
        "grantedDate": "01/03/2000",
        "effectiveDate": "01/04/2000",
        "endDate": "01/05/2000",
        "operatorName": "Blue Sky Buses",
        "busServiceTypeId": "Limited",
        "busServiceTypeDescription": "Limited Stopping",
        "trafficAreaId": "D",
        "applicationType": "Change",
        "publicationText": "Change of Route",
        "otherDetails": "Operates only on weekdays",
    }

    # Assert that the object is valid
    try:
        Registration.model_validate(registration_data)

        # Create the registration object
        registration = Registration(**registration_data)

        # Assert that the object is created successfully
        assert isinstance(registration, Registration)
    except ValidationError:
        assert False, "Registration object is not valid"
