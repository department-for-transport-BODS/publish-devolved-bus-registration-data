from unittest.mock import MagicMock
from managers.csv_manager import CSVManager
from utils.pydant_model import AuthenticatedEntity

_mock_entity = AuthenticatedEntity(type="user", name="testuser", group="testgroup")


def test_validation_and_insertion_steps():
    # Arrange
    data = "license_number,name\n123,John Doe\n456,Jane Smith\n789,Invalid Record"
    csv_manager = CSVManager(data, authenticated_entity=_mock_entity)
    csv_manager._validate_csv_data = MagicMock(
        return_value={
            "valid_records": {
                "2": MagicMock(),
                "3": MagicMock(),
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
    csv_manager._send_report_to_db = MagicMock()
    csv_manager._check_duplicate_records = MagicMock()
    csv_manager._remove_licence_details = MagicMock(
        return_value={
            "valid_records": [{"license_number": "123", "name": "John Doe"}],
            "invalid_records": [{"license_number": "456", "name": "Invalid Record"}],
        }
    )

    # Act
    csv_manager.validation_and_insertion_steps()

    # Assert — function returns None (sends report to DB, no return value)
    csv_manager._validate_csv_data.assert_called_once()
    csv_manager._check_duplicate_records.assert_called_once()
    csv_manager._check_licence_number_existence.assert_called_once()
    csv_manager._send_to_db.assert_called_once()
    csv_manager._remove_licence_details.assert_called_once()
    csv_manager._send_report_to_db.assert_called_once()


def test_validate_csv_data():
    # Arrange
    data = "license_number,name\n123,John Doe\n456,Jane Smith\n789,Invalid Record"
    csv_manager = CSVManager(data, authenticated_entity=_mock_entity)
    csv_manager._validate_csv_data = MagicMock(
        return_value={
            "valid_records": [
                {"license_number": "123", "name": "John Doe"},
                {"license_number": "456", "name": "Jane Smith"},
            ],
            "invalid_records": [{"license_number": "789", "name": "Invalid Record"}],
        }
    )
    records = csv_manager._validate_csv_data()
    csv_manager._check_licence_number_existence = MagicMock(
        return_value={"valid_records": {}, "invalid_records": {}}
    )

    # Act
    result = csv_manager._check_licence_number_existence(records)

    # Assert
    assert result == {"valid_records": {}, "invalid_records": {}}
