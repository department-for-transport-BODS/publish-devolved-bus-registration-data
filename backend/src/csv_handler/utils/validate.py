from .custom_exception import LicenceDetailsError
from .pydant_model import LicenceRecord

from .logger import log
from .api import verify_otc_api
import traceback


# get licenceRecord that has licence_number x001
def licence_detail(licence_number, licence_details):
    return next(
        (
            record
            for record in licence_details
            # if record.licence_number == licence_number
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
    validated_records = uploaded_records["valid_records"]
    # otc_API_response = MockData.mock_otc_licencd_and_operator_api(validated_records)
    # otc_api_response = verify_otc_api(validated_records)
    # sys.exit()

    # {licence_number:.....,licence_details:{licence_number:.....,Licence_status:.....},operator_details:{operator_name:.....}}
    mocked_list = []
    for licence in validated_records:
        mocked_list.append(
            {
                "licence_number": licence,
                "licence_details": {"licence_number": "1", "licence_status": "valid"},
                "operator_details": {"operator_name": "test operator"},
            }
        )

    try:
        # licence_details = [
        #     LicenceRecord(**record) for record in otc_api_response["licences"]
        # ]
        licence_details = [LicenceRecord(**record) for record in mocked_list]

    except Exception as e:
        traceback.print_exc()
        log.error(f"Error: {e}")

    valid_records = {}
    invalid_records = {}
    for idx, record in uploaded_records["valid_records"].items():
        print("record")
        print(record)
        try:
            # Get licence details
            licence = licence_detail(record.licence_number, licence_details)
            if (
                licence is None
                or licence.licence_details is None
                or licence.operator_details is None
            ):
                invalid_records[idx] = [
                    {"LicenceNumber": "Licence number is not found in the OTC DB"}
                ]
            else:

                # Add the licence details to the record
                valid_records.update({idx: [record, licence]})

        except Exception as e:
            log.error(f"Error: {e}")

    uploaded_records["valid_records"] = valid_records
    if len(invalid_records) > 0:
        uploaded_records["invalid_records"].append(
            {
                "records": invalid_records,
                "description": "Warning - Record failed due to OTC validation",
            }
        )
