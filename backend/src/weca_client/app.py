from utils.weca_api import WecaClient
from utils.pydant_model import AuthenticatedEntity
from managers.records_manager import RecordsManager
from utils.settings import USER_TYPE, USER_NAME, USER_GROUP


class WecaManager:
    def __init__(self):
        api_client = WecaClient()
        self.api_response = api_client.fetch_weca_services()



def main():
    print("Weca API is running")
    authenticated_entity = AuthenticatedEntity(type=USER_TYPE, name=USER_NAME, group=USER_GROUP)
    weca = WecaManager()
    received_data = weca.api_response.data
    print("Received data: ", received_data[0])
    RecordsManager(received_data, authenticated_entity).validation_and_insertion_steps()
    print("Weca API has finished running")

    

main()