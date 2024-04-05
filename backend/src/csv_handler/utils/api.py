from typing import List
import requests
from .logger import log
import json
from central_config import OTC_CLIENT_API_URL


def verify_otc_api(licence_numbers: List):
    """
    This function sends a list of licence numbers to the OTC api.

    Args:
        licence_numbers (List): A list of licence numbers.

    Returns:
        [dict]: For eact found licence, with a licence details.
    """
    try:
        licence_numbers_list = set()
        log.info("Sending list to OTC API")
        for key, registration in licence_numbers.items():
            licence_numbers_list.add(registration.licence_number)

        if OTC_CLIENT_API_URL != "OTC_API_URL is not set":
            url = OTC_CLIENT_API_URL
        else:
            raise Exception("OTC_API_URL is not set")
        response = requests.post(
            url,
            data=json.dumps(list(licence_numbers_list)),
            headers={"Content-Type": "application/json"},
        )
        # add a list as body of the request
        if response.status_code == 200:
            print("List sent successfully!")
            output = response.json()
            return output
        else:
            print("Failed to send list. Error:", response.status_code)
            print(response)
    except Exception as e:
        print(e)
