from .custom_exception import LicenceDetailsError
from .mocker import MockData
from .pydant_model import LicenceRecord

from .logger import log,console


# get licenceRecord that has licence_number x001
def licence_detail(licence_number, licence_details):
    return next(
        (
            record

            for record in licence_details
            if record.licence_number == licence_number
        ),
        None,
    )


def validate_licence_number_existence(uploaded_records: dict):
    """
    This function takes a list of licence numbers and checks if they exist in the database.

    Args:
        uploaded_records (dict): A dictionary containing the records to be validated.

    Returns:
        [list]: A list of dictionaries containing the details of the licences.
    """
    # Collect all the licence numbers from the records
    validated_rocords = uploaded_records["valid_records"]
    console.log(validated_rocords)
    otc_API_response = MockData.mock_otc_licencd_and_operator_api(validated_rocords)

    try:
        licence_details = [
            LicenceRecord(**record) for record in otc_API_response["licences"]
        ]

    except Exception as e:
        log.error(f"Error: {e}")

    valid_records = {}
    for idx, record in uploaded_records["valid_records"].items():
        try:
            # Get licence details
            licence = licence_detail(record.licence_number, licence_details)
            if (
                licence is None
                or licence.licence_details is None
                or licence.operator_details is None
            ):
                raise LicenceDetailsError

            # Add the licence details to the record
            valid_records.update({idx: [record, licence]})

        except LicenceDetailsError:
            if idx not in uploaded_records["invalid_records"]:
                uploaded_records["invalid_records"].update(
                    {
                        idx: [
                            {
                                "LicenceNumber": "Licence number is not found in the OTC DB"
                            }
                        ]
                    }
                )
            else:
                uploaded_records["invalid_records"][idx].append(
                    {"LicenceNumber": "Licence number is not found in the OTC DB"}
                )
        except Exception as e:
            log.error(f"Error: {e}")
        finally:
            uploaded_records["valid_records"] = valid_records

    return uploaded_records
