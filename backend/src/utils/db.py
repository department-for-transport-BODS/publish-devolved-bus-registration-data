import os
from sys import exit
from typing import List

import boto3
import psycopg2
from sqlalchemy import create_engine, select
# from .db.models import EPRegistration, OTCOperator, OTCLicence
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from .csv_validator import Registration
from .logger import console, log
from .validate import validate_licence_number_existence


class CreateEngine:
    @staticmethod
    def get_engine():
        DB_HOST = os.environ.get("DB_HOST", "localhost")
        DB_PORT = os.environ.get("DB_PORT", "5433")
        DB_USER = os.environ.get("DB_USER", "postgres")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
        DB_NAME = os.environ.get("DB_NAME", "postgres")
        engine = None

        try:
            engine = create_engine(
                f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            )
            connection = engine.connect()
            print("Connection to PostgreSQL DB successful")
            connection.close()
        except Exception as e:
            print(f"The error '{e}' occurred")
            exit(1)
        return engine


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


engine = CreateEngine.get_engine()


def add_or_get_record(column_name: str, value: str, session: Session, Model, record):
    """
    Add a new record to the table if it doesn't exist, or get the id of the existing record.
    """
    try:
        stmt = select(Model).where(getattr(Model, column_name) == value)
        if not session.query(stmt.exists()).scalar():
            new_record = record
            session.add(new_record)
            session.flush()
            log.debug(f"New added record id: {new_record.id}, to table: {Model}")
            session.commit()
            return new_record.id
        else:
            existing_record = (
                session.query(Model).filter(getattr(Model, column_name) == value).first()
            )
            return existing_record.id
    except Exception as e:
        log.error(f"Error: {e}")
        session.rollback()
        return None


class AutoMappingModels:
    def __init__(self):
        self.engine = CreateEngine.get_engine()
        self.Base = automap_base()
        self.Base.prepare(autoload_with=engine)
        self.EPRegistration = self.Base.classes.ep_registration
        self.OTCOperator = self.Base.classes.otc_operator
        self.OTCLicence = self.Base.classes.otc_licence
        self.OTCLicence.__repr__ = (
            lambda self: f"<OTCLicence(licence_number='{self.licence_number}', licence_status='{self.licence_status}, otc_licence_id={self.otc_licence_id}')>"
        )
        self.OTCOperator.__repr__ = (
            lambda self: f"<OTCOperator(operator_name='{self.operator_name}', operator_id='{self.operator_id}')>"
        )
        self.EPRegistration.__repr__ = (
            lambda self: f"<EPRegistration(route_number='{self.route_number}', route_description='{self.route_description}', variation_number='{self.variation_number}', start_point='{self.start_point}', finish_point='{self.finish_point}', via='{self.via}', subsidised='{self.subsidised}', subsidy_detail='{self.subsidy_detail}', is_short_notice='{self.is_short_notice}', received_date='{self.received_date}', granted_date='{self.granted_date}', effective_date='{self.effective_date}', end_date='{self.end_date}', otc_operator_id='{self.otc_operator_id}', bus_service_type_id='{self.bus_service_type_id}', bus_service_type_description='{self.bus_service_type_description}', registration_number='{self.registration_number}', traffic_area_id='{self.traffic_area_id}', application_type='{self.application_type}', publication_text='{self.publication_text}', other_details='{self.other_details}')>"
        )

    def get_tables(self):
        return {
            "EPRegistration": self.EPRegistration,
            "OTCOperator": self.OTCOperator,
            "OTCLicence": self.OTCLicence,
        }


class DBManager:
    @classmethod
    def fetch_operator_record(
        cls, operator_name: str, session: Session, OTCOperator, operator_record
    ):
        operator_record_id = add_or_get_record(
            "operator_name", operator_name, session, OTCOperator, operator_record
        )
        return operator_record_id

    @classmethod
    def fetch_licence_record(
        cls, licence_number: str, session: Session, OTCLicence, licence_record
    ):
        console.log(f"licence_number: {licence_number}")
        licence_record_id = add_or_get_record(
            "licence_number", licence_number, session, OTCLicence, licence_record
        )
        console.log(f"otc_licence_id: {licence_record_id}")
        return licence_record_id

    @classmethod
    def add_record_to_ep_registration_table(
        cls,
        record: Registration,
        operator_record_id: int,
        licence_record_id: int,
        session: Session,
        EPRegistration,
    ):
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
            bus_service_type_id=record.bus_service_type_id,
            bus_service_type_description=record.bus_service_type_description,
            registration_number=record.registration_number,
            traffic_area_id=record.traffic_area_id,
            application_type=record.application_type,
            publication_text=record.publication_text,
            other_details=record.other_details,
            otc_operator_id=operator_record_id,
            otc_licence_id=licence_record_id,
        )
        session.add(ep_registration_record)
        session.flush()
        console.log(f"New EP registration record: {ep_registration_record.id}")




def send_to_db(validated_records: List[Registration]):
    # validated_records: List[Registration] = MockData.mock_user_csv_record()
    tables = AutoMappingModels().get_tables()
    OTCOperator = tables["OTCOperator"]
    OTCLicence = tables["OTCLicence"]
    EPRegistration = tables["EPRegistration"]
    # Check if the licence number exists in the OTC database
    # validated_records = validate_licence_number_existence(validated_records)
    
    for idx, record_and_licence in validated_records["valid_records"].items():
        try:
            record, licence = record_and_licence
            OTCOperator_record = OTCOperator(
                operator_name=licence.operator_details.operator_name,
                operator_id=licence.operator_details.operator_id,
            )
            session = Session(engine)
            operator_record_id = DBManager.fetch_operator_record(
                licence.operator_details.operator_name,
                session,
                OTCOperator,
                OTCOperator_record,
            )

            OTCLicence_recrod = OTCLicence(
                licence_number=licence.licence_details.licence_number,
                licence_status=licence.licence_details.licence_status,
                otc_licence_id=licence.licence_details.otc_licence_id,
            )
            licence_record_id = DBManager.fetch_licence_record(
                licence.licence_details.licence_number,
                session,
                OTCLicence,
                OTCLicence_recrod,
            )

            DBManager.add_record_to_ep_registration_table(
                record, operator_record_id, licence_record_id, session, EPRegistration
            )

            session.commit()
        except Exception:
            console.print_exception(show_locals=False)
            session.rollback()
        finally:
            session.close()