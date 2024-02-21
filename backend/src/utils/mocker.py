
from typing import List

from .pydant_model import Registration


class MockData:
    @classmethod
    def mock_otc_licencd_and_operator_api(cls, licence_numbers: List[str]) -> dict:
        # Mockk an API call to get the licence status and operator name
        return {
            "licences": [
                {
                    "licence_number": "PC7654322",
                    "licence_details": {
                        "licence_number": "string",
                        "licence_status": "string",
                        "otc_licence_id": 123,
                    },
                    "operator_details": {
                        "operator_name": "string",
                        "otc_operator_id": 123,

                    },
                },
                {
                    "licence_number": "x001",
                    "licence_details": None,
                    "operator_details": None,
                },
            ]
        }

    @classmethod
    def mock_user_csv_record(cls):
        reg_record = Registration(
            licenceNumber="PC7654322",
            registrationNumber="PD7654321/87654321",
            routeNumber="2",
            routeDescription="City Center - Suburb - Main Street",
            variationNumber=1,
            startPoint="City Center",
            finishPoint="Suburb",
            via="Main Street",
            subsidised="Fully",
            subsidyDetail="Transport for Local Authority (LA)",
            isShortNotice=False,
            receivedDate="01/01/2000",
            grantedDate="01/02/2000",
            effectiveDate="01/03/2000",
            endDate="01/04/2000",
            operatorName="Blue Sky Buses",
            busServiceTypeId="Standard",
            busServiceTypeDescription="Normal Stopping",
            trafficAreaId="C",
            applicationType="New",
            publicationText="Revised timetable to improve reliability",
            otherDetails="",
        )
        reg_record2 = Registration(
            licenceNumber="x002",
            registrationNumber="PD7654321/87654321",
            routeNumber="2",
            routeDescription="City Center - Suburb - Main Street",
            variationNumber=1,
            startPoint="City Center",
            finishPoint="Suburb",
            via="Main Street",
            subsidised="Fully",
            subsidyDetail="Transport for Local Authority (LA)",
            isShortNotice=False,
            receivedDate="01/01/2000",
            grantedDate="01/02/2000",
            effectiveDate="01/03/2000",
            endDate="01/04/2000",
            operatorName="Blue Sky Buses",
            busServiceTypeId="Standard",
            busServiceTypeDescription="Normal Stopping",
            trafficAreaId="C",
            applicationType="New",
            publicationText="Revised timetable to improve reliability",
            otherDetails="",
        )
        return [reg_record, reg_record2]

