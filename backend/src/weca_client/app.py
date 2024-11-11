from managers.records_manager import RecordsManager
from utils.pydant_model import AuthenticatedEntity
from utils.settings import USER_TYPE, USER_NAME, USER_GROUP
from utils.weca_api import WecaClient


class WecaManager:
    def __init__(self):
        api_client = WecaClient()
        self.api_response = api_client.fetch_weca_services()


def lambda_handler(event, context):
    print("WECA API ingestion is running")
    authenticated_entity = AuthenticatedEntity(
        type=USER_TYPE, name=USER_NAME, group=USER_GROUP
    )
    weca = WecaManager()
    received_data = weca.api_response.data
    print("Received data: ", received_data[0])
    RecordsManager(received_data, authenticated_entity).validation_and_insertion_steps()
    print("Weca API ingestion has finished running")
