from unittest.mock import MagicMock
from managers.csv_manager import CSVManager
from utils.pydant_model import Registration


mocked_registration = Registration(license_number="123", name="John Doe")


def test_validation_and_insertion_steps():
    # Arrange
    data = "license_number,name\n123,John Doe\n456,Jane Smith\n789,Invalid Record"
    csv_manager = CSVManager(data)
    csv_manager._validate_csv_data = MagicMock(
        return_value={
            "valid_records": {
                "2": Registration(
                    license_number="123",
                    name="John Doe",
                    variation_number="1",
                    registration_number="123",
                    operator_name="John Doe",
                    operator_address="123",
                    operator_postcode="123",
                    operator_contact="123",
                    operator_email="123",
                    operator_phone="123",
                ),
                "3": Registration(
                    license_number="456",
                    name="Jane Smith",
                    variation_number="1",
                    registration_number="123",
                    operator_name="John Doe",
                    operator_address="123",
                    operator_postcode="123",
                    operator_contact="123",
                    operator_email="123",
                    operator_phone="123",
                ),
            },
            "invalid_records": {
                "4": [{"license_number": "789", "name": "Invalid Record"}]
            },
        }
    )
    csv_manager._check_licence_number_existence = MagicMock(
        return_value={
            "valid_records": [{"license_number": "123", "name": "John Doe"}],
            "invalid_records": [{"license_number": "456", "name": "Invalid Record"}],
        }
    )
    csv_manager._send_to_db = MagicMock()
    csv_manager._remove_licence_details = MagicMock(
        return_value={
            "valid_records": [{"license_number": "123", "name": "John Doe"}],
            "invalid_records": [{"license_number": "456", "name": "Invalid Record"}],
        }
    )

    # Act
    result = csv_manager.validation_and_insertion_steps()

    # Assert
    assert result == {
        "invalid_records": [{"license_number": "456", "name": "Invalid Record"}],
        "valid_records_count": 1,
    }
    csv_manager._validate_csv_data.assert_called_once()
    csv_manager._check_licence_number_existence.assert_called_once()
    csv_manager._send_to_db.assert_called_once()
    csv_manager._remove_licence_details.assert_called_once()


def test_validate_csv_data():
    # Arrange
    data = "license_number,name\n123,John Doe\n456,Jane Smith\n789,Invalid Record"
    csv_manager = CSVManager(data)
    csv_manager._validate_csv_data = MagicMock(
        return_value={
            "valid_records": {
                {"license_number": "123", "name": "John Doe"},
                {"license_number": "456", "name": "Jane Smith"},
            },
            "invalid_records": [{"license_number": "789", "name": "Invalid Record"}],
        }
    )
    records = csv_manager._validate_csv_data()
    # Act
    result = csv_manager._check_licence_number_existence(records)

    # Assert
    assert result == {"valid_records": {}, "invalid_records": {}}
