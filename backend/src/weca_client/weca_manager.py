from utils.weca_api import WecaClient
from utils.logger import console
from utils.pydant_model import AuthenticatedEntity
from managers.records_manager import RecordsManager

received_data = {
    "id": "554",
    "registrationNumber": 'PH0006633/01010001',
    "variationNumber": '5',
    "licenceNumber": 'PH0006633',
    "serviceNumber": 'Excursion',
    "startPoint": 'weca test api',
    "finishPoint": 'CIRCULAR',
    "via": 'QUEEN SQUARE',
    "effectiveDate": "01/01/2000", 
    "apiType": 'WECA',
    "atco_code": '010',
    "routeNumber": "2",
    "routeDescription": "City Center - Suburb - Main Street",
    "description": "City Center - Suburb - Main Street",
    "subsidised": "Fully",
    "subsidyDetail": "Transport for Local Authority (LA)",
    "isShortNotice": False,
    "receivedDate": "01/01/2000",
    "grantedDate": "01/02/2000",
    "endDate": "01/04/2000",
    "operatorName": "Blue Sky Buses",
    "busServiceTypeId": "Standard",
    "busServiceTypeDescription": "Normal Stopping",
    "trafficAreaId": "C",
    "applicationType": "New",
    "publicationText": "Revised timetable to improve reliability",
    "otherDetails": ""
}

class WecaManager:
    def __init__(self):
        api_client = WecaClient()
        self.api_response = api_client.fetch_weca_services()
        # console.log(self.api_response.data[0])
        # self.received_data = self.api_response.data
        # self.received_data = [received_data]




# authenticated_entity = AuthenticatedEntity(type="user", name="weca_api", group="weca")
WecaManager()
# RecordsManager([received_data], authenticated_entity).validation_and_insertion_steps()

    


# weca = WecaManager()

# console.log(weca.received_data)