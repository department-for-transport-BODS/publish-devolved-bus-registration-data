import os

import boto3
import psycopg2
from .logger import log
from sqlalchemy.orm import Session
from .csv_validator import Registration
from sqlalchemy import select

# from .db.models import EPRegistration, OTCOperator, OTCLicence
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from rich.logging import RichHandler
import logging
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log2 = logging.getLogger("rich")
from rich.console import Console
console = Console()
def connect_to_db():
    # Connect to the database
    dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
    table = dynamodb.Table("your_table_name")

    return table


def get_results_db_conn():
    conn = None
    environment = os.environ.get("PROJECT_ENV", "localdev")
    log.debug(f"env: {environment}")
    if environment != "localdev":
        log.info("Using argo environment")
        aws_region = os.getenv("REGION", "eu-west-2")
        session = boto3.session.Session()
        rds = session.client(service_name="rds", region_name=aws_region)
        os.environ["POSTGRES_TOKEN"] = rds.generate_db_auth_token(
            DBHostname=os.environ.get("POSTGRES_HOST"),
            Port=int(os.environ.get("POSTGRES_PORT")),
            DBUsername=os.environ.get("POSTGRES_USER"),
            Region=aws_region,
        )
    log.info(f'Automation host: {os.environ.get("POSTGRES_HOST")}')
    log.info(f'Automation port: {os.environ.get("POSTGRES_PORT")}')
    log.info(f'Automation user: {os.environ.get("POSTGRES_USER")}')
    log.info(f'Automation DB: {os.environ.get("POSTGRES_DATABASE")}')
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", "5433"),
        database=os.environ.get("POSTGRES_DATABASE", "postgres"),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_TOKEN", "postgres"),
    )
    if conn is not None:
        print("Connection established to PostgreSQL.")
    else:
        print("Connection not established to PostgreSQL.")
    return conn


def create_item(table, item):
    # Create a new item in the database
    response = table.put_item(Item=item)
    return response


def read_item(table, key):
    # Read an item from the database
    response = table.get_item(Key=key)
    item = response.get("Item")
    return item


def update_item(table, key, update_expression, expression_attribute_values):
    # Update an item in the database
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
    return response


def delete_item(table, key):
    # Delete an item from the database
    response = table.delete_item(Key=key)
    return response


def connect_to_db_using_sqlalchemy():
    # Connect to the database using SQLAlchemy
    from sqlalchemy import create_engine

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5433")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
    DB_NAME = os.environ.get("DB_NAME", "postgres")

    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # engine = sqlalchemy.create_engine(os.environ.get("DATABASE_URL"))

    # check if the connection is successful
    try:
        connection = engine.connect()
        print("Connection to PostgreSQL DB successful")
        connection.close()
    except Exception as e:
        print(f"The error '{e}' occurred")
    return engine


engine = connect_to_db_using_sqlalchemy()
# Base.metadata.create_all(engine)


def insert_into_EPRegistration(engine, registration):
    # Insert a new record into the EPRegistration table
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(registration)
    session.commit()
    session.close()


data = {
    "route_number": "1",
    "route_description": "Test route",
    "variation_number": 1,
    "start_point": "Start",
    "finish_point": "Finish",
    "via": "Via",
    "subsidised": "Yes",
    "subsidy_detail": "Subsidy detail",
    "is_short_notice": False,
    "received_date": "2021-01-01",
    "granted_date": "2021-01-01",
    "effective_date": "2021-01-01",
    "end_date": "2021-01-01",
    "otc_operator_id": 1,
    "bus_service_type_id": "1",
    "bus_service_type_description": "Test bus service",
    "registration_number": "1",
    "traffic_area_id": "1",
    "application_type": "Test application",
    "publication_text": "Test publication",
    "other_details": "Test other details",
}


def add_or_get_record(column_name: str, value: str, session: Session, Model, record):
    """
    Add a new record to the table if it doesn't exist, or get the id of the existing record.
    """
    console.log(record)
    console.log(f"Column name: {column_name}")
    console.log(f"Value: {value}")
    stmt = select(Model).where(getattr(Model, column_name) == value)

    if not session.query(stmt.exists()).scalar():
        new_record = record
        session.add(new_record)
        session.flush()
        log.debug(f"New added record id: {new_record.id}")
        session.commit()
        return new_record.id
    else:
        existing_record = (
            session.query(Model).filter(getattr(Model, column_name) == value).first()
        )
        return existing_record.id


def add_record_to_table_using_sql_query():
    # Add a new record to the table using a SQL query
    with engine.connect() as connection:
        print(
            "Connection established to PostgreSQL. Adding record to table using SQL query."
        )
        connection.execute(
            "INSERT INTO ep_registration (route_number, route_description, variation_number, start_point, finish_point, via, subsidised, subsidy_detail, is_short_notice, received_date, granted_date, effective_date, end_date, otc_operator_id, bus_service_type_id, bus_service_type_description, registration_number, traffic_area_id, application_type, publication_text, other_details) VALUES ('1', 'Test route', 1, 'Start', 'Finish', 'Via', 'Yes', 'Subsidy detail', False, '2021-01-01', '2021-01-01', '2021-01-01', '2021-01-01', 1, '1', 'Test bus service', '1', '1', 'Test application', 'Test publication', 'Test other details')"
        )


# function to add to otc_operator table
def add_record_to_otc_operator_table():
    # Add a new record to the table using orm method
    with engine.connect() as connection:
        print(
            "Connection established to PostgreSQL. Adding record to table using SQL query."
        )
        connection.execute(
            otc_operator.insert().values(operator_name="Test operator", operator_id=3)
        )
        # commit the transaction
        connection.commit()
    # Add a new record to the ep_registration table using orm method
    with engine.connect() as connection:
        print(
            "Connection established to PostgreSQL. Adding record to table using SQL query."
        )
        connection.execute(
            ep_reg.insert().values(
                route_number="1",
                route_description="Test route",
                variation_number=1,
                start_point="Start",
                finish_point="Finish",
                via="Via",
                subsidised="Yes",
                subsidy_detail="Subsidy detail",
                is_short_notice=False,
                received_date="2021-01-01",
                granted_date="2021-01-01",
                effective_date="2021-01-01",
                end_date="2021-01-01",
                otc_operator_id=10,
                bus_service_type_id="1",
                bus_service_type_description="Test bus service",
                registration_number="1",
                traffic_area_id="1",
                application_type="Test application",
                publication_text="Test publication",
                other_details="Test other details",
            )
        )
        connection.commit()


def add_record_to_otc_operator_table_using_orm():
    # Add a new record to the table using orm method
    new_record = Registration(**data)
    print(new_record)


def read_recrod_from_otc_operator_table():
    # Read a record from the table
    with Session(engine) as session:
        statement = select(OTCOperator)
        # result = session.scalars(statement)
        for row in session.scalars(statement):
            print(row)


def do_this():
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if the license number exists
    license_number = "YOUR_LICENSE_NUMBER"
    otc_license = (
        session.query(OTCLicence).filter_by(licence_number=license_number).first()
    )

    # If the license number doesn't exist, create a new OTC license
    if not otc_license:
        otc_license = OTCLicence(licence_number=license_number)
        session.add(otc_license)
        session.commit()

    # Check if the OTC operator exists
    operator_id = "YOUR_OPERATOR_ID"
    otc_operator = session.query(OTCOperator).filter_by(operator_id=operator_id).first()

    # If the OTC operator doesn't exist, create a new OTC operator
    if not otc_operator:
        otc_operator = OTCOperator(operator_id=operator_id)
        session.add(otc_operator)
        session.commit()

    # Create a new EP registration record with the OTC license ID and OTC operator ID
    ep_registration = EPRegistration(
        otc_licence_id=otc_license.id,
        otc_operator_id=otc_operator.id,
        # Add other EP registration data here
    )

    session.add(ep_registration)
    session.commit()


def auto_mapping_models():
    # Automap the database
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    # Create a session
    # Session = sessionmaker(engine)
    # Access the tables
    EPRegistration = Base.classes.ep_registration
    OTCOperator = Base.classes.otc_operator
    OTCLicence = Base.classes.otc_licence
    EPRegistration.__repr__ = (
        lambda self: f"<EPRegistration(route_number='{self.route_number}', route_description='{self.route_description}', variation_number='{self.variation_number}', start_point='{self.start_point}', finish_point='{self.finish_point}', via='{self.via}', subsidised='{self.subsidised}', subsidy_detail='{self.subsidy_detail}', is_short_notice='{self.is_short_notice}', received_date='{self.received_date}', granted_date='{self.granted_date}', effective_date='{self.effective_date}', end_date='{self.end_date}', otc_operator_id='{self.otc_operator_id}', bus_service_type_id='{self.bus_service_type_id}', bus_service_type_description='{self.bus_service_type_description}', registration_number='{self.registration_number}', traffic_area_id='{self.traffic_area_id}', application_type='{self.application_type}', publication_text='{self.publication_text}', other_details='{self.other_details}')>"
    )
    # Add __repr__ method to the class OTCOperator
    OTCOperator.__repr__ = (
        lambda self: f"<OTCOperator(operator_name='{self.operator_name}', operator_id='{self.operator_id}')>"
    )
    # Add __repr__ method to the class OTCLicence
    OTCLicence.__repr__ = (
        lambda self: f"<OTCLicence(licence_number='{self.licence_number}', licence_status='{self.licence_status}, otc_licence_id={self.otc_licence_id}')>"
    )
    return {
        "EPRegistration": EPRegistration,
        "OTCOperator": OTCOperator,
        "OTCLicence": OTCLicence,
    }

    # Get recirds in regsitration table
    # with Session() as session:
    #     statement = select(EPRegistration)
    #     # result = session.scalars(statement)
    #     for row in session.scalars(statement):
    #         print(row)


def licence_status_licence_id_and_op_name(licence_number: str) -> dict:
    # Mockk an API call to get the licence status and operator name
    return {
        "otc_licence_id": 36,
        "licence_status": "active",
        "operator_name": "Test operator8",
        "operator_id": 4,
    }


from typing import List


def mock_data():
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
    send_to_db([reg_record])



def send_to_db(validated_records: List[Registration]):

    tables = auto_mapping_models()
    OTCOperator = tables["OTCOperator"]
    OTCLicence = tables["OTCLicence"]
    EPRegistration = tables["EPRegistration"]

    for record in validated_records:
        try:
            session = Session(engine)
            operator_record_id = add_record_to_otc_operator_table(record, session, OTCOperator)
            licence_record_id = add_record_to_otc_licence_table(record, session, OTCLicence)
            add_record_to_ep_registration_table(record, operator_record_id, licence_record_id, session, EPRegistration)
            session.commit()
        except Exception:
            console.print_exception(show_locals=True)
            session.rollback()
        finally:
            session.close()

def add_record_to_otc_operator_table(record: Registration, session: Session,OTCOperator) -> int:
    operator_id = licence_status_licence_id_and_op_name(record.licence_number)["operator_id"]
    operator_name = licence_status_licence_id_and_op_name(record.licence_number)["operator_name"]
    console.log(f"Operator name: {operator_name}")
    operator_record = OTCOperator(operator_name=operator_name, operator_id=operator_id)
    operator_record_id = add_or_get_record("operator_name", operator_name, session, OTCOperator, operator_record)
    console.log(f"New operator record: {operator_record_id}")
    return operator_record_id

def add_record_to_otc_licence_table(record: Registration, session: Session,OTCLicence) -> int:
    licence_number = record.licence_number
    otc_licence_status = licence_status_licence_id_and_op_name(licence_number)["licence_status"]
    otc_licence_id = licence_status_licence_id_and_op_name(licence_number)["otc_licence_id"]
    licence_record = OTCLicence(licence_number=licence_number, licence_status=otc_licence_status, otc_licence_id=otc_licence_id)
    licence_record_id = add_or_get_record("licence_number", licence_number, session, OTCLicence, licence_record)
    console.log(f"otc_licence_id: {licence_record_id}")
    return licence_record_id

def add_record_to_ep_registration_table(record: Registration, operator_record_id: int, licence_record_id: int, session: Session, EPRegistration):
    ep_registration_record = EPRegistration(
        route_number=record.route_number,
        route_description=record.route_description,
        variation_number=record.variation_number,
        start_point=record.start_point,
        finish_point=record.finish_point,
        via=record.via,
        subsidised=record.subsidised,
        subsidy_detail=record.subsidy_detail,
        is_short_notice=record.is_short_notice,
        received_date=record.received_date,
        granted_date=record.granted_date,
        effective_date=record.effective_date,
        end_date=record.end_date,
        otc_operator_id=operator_record_id,
        bus_service_type_id=record.bus_service_type_id,
        bus_service_type_description=record.bus_service_type_description,
        registration_number=record.registration_number,
        traffic_area_id=record.traffic_area_id,
        application_type=record.application_type,
        publication_text=record.publication_text,
        other_details=record.other_details,
        otc_licence_id=licence_record_id,
    )
    session.add(ep_registration_record)
    console.log(f"New EP registration record: {ep_registration_record.id}")

