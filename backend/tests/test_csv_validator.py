from pydantic import ValidationError

from src.utils.csv_validator import (Registration,
                                     extract_field_mgs_type_from_errors)


def test_extract_field_mgs_type_from_errors():
    # Create a ValidationError object with sample errors
    errors = [
        {
            "loc": ["first_name"],
            "msg": "Field required",
            "type": "missing",
            "ctx": {"limit_value": 1},
            "url": "dummy url"
        },
        {
            "msg": "Field required",
            "type": "missing"
        },
        {
            "loc": ["address"],
            "type": "missing"
        }
    ]
    # validation_error = ValidationError(errors)

    # Call the function and get the result
    result = extract_field_mgs_type_from_errors(errors)

    # Assert that the result matches the expected output
    expected_result = [
        {
            "field": ["first_name"],
            "message": "Field required",
            "type": "missing"
        },
        {
            "field": None,
            "message": "Field required",
            "type": "missing"
        },
        {
            "field": ["address"],
            "message": None,
            "type": "missing"
        }
    ]
    assert result == expected_result

def test_registration_model():
    # Create a valid registration object
    registration_data = {
        "licenceNumber": "PC2021320",
        "registrationNumber": "PD0001111/43010100",
        "routeNumber": "1",
        "routeDescription": "Wigan - Highfield Grange Circular",
        "variationNumber": 1,
        "startPoint": "Wigan",
        "finishPoint": "Highfield Grange Circular",
        "via": "",
        "subsidised": True,
        "subsidyDetail": "Transport for Greater Manchester (TFGM)",
        "isShortNotice": False,
        "receivedDate": "09/01/2023",
        "grantedDate": "09/01/2023",
        "effectiveDate": "9/24/2023",
        "endDate": "8/31/2028",
        "operatorId": "1028807",
        "busServiceTypeId": "Standard",
        "busServiceTypeDescription": "Normal Stopping",
        "trafficAreaId": "C",
        "applicationType": "New",
        "publicationTest": "Revised timetable to improve reliability",
        "otherDetails": None
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