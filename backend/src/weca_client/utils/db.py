import boto3
import json
import urllib.parse
from os import getenv
from typing import List
from sqlalchemy import create_engine, select, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from .data import common_keys_comparsion
from .exceptions import (
    GroupIsNotFound,
    RecordIsAlreadyExist,
    RecordBelongsToAnotherUser,
)
from .logger import log
from .pydant_model import DBCreds, Registration
from .settings import AWS_REGION, ENVIRONMENT


class CreateEngine:
    @staticmethod
    def generate_connection_string(**kwargs) -> str:
        """
        Generates an AWS RDS IAM authentication token for a given RDS instance.

        Parameters:
        - **kwargs (any): A dictionary of key/value pairs that correspond to the expected values below

        Returns:
        - str: The generated connection string from parsed key/value pairs
        """
        user_password = ""
        if kwargs.get("user"):
            user_password += kwargs.get("user")
            if kwargs.get("password"):
                user_password += ":" + kwargs.get("password")
            user_password += "@"

        # Construct other parts
        other_parts = ""
        for key, value in kwargs.get("optargs").items():
            if key not in ["host", "port", "user", "password", "dbname"] and value:
                other_parts += f"{key}={value}&"

        # Construct the final connection string
        connection_string = f"postgresql+psycopg2://{user_password}{kwargs.get('host', '')}"
        if kwargs.get("port"):
            connection_string += f":{kwargs.get('port')}"
        connection_string += f"/{kwargs.get('dbname', '')}"
        if other_parts:
            connection_string += f"?{other_parts[:-1]}"
        return connection_string

    @staticmethod
    def generate_rds_iam_auth_token(host, port, username) -> str:
        """
        Generates an AWS RDS IAM authentication token for a given RDS instance.

        Parameters:
        - hostname (str): The endpoint of the RDS instance.
        - port (int): The port number for the RDS instance.
        - username (str): The database username.

        Returns:
        - str: The generated IAM authentication token if successful.
        - None: If an error occurs during token generation.
        """
        try:
            session = boto3.session.Session()
            client = session.client(
                service_name="rds",
                region_name=AWS_REGION
            )
            token = client.generate_db_auth_token(
                DBHostname=host,
                DBUsername=username,
                Port=port
            )
            return urllib.parse.quote_plus(token)
        except Exception as e:
            log.error(f"An error occurred while generating the IAM auth token: {e}")
            return None

    @staticmethod
    def get_credentials():
        """
        Method to get the connection details for the database
        """
        creds = DBCreds(password="initial")
        try:
            if ENVIRONMENT != "local":
                log.debug("Getting DB token")
                creds.password = CreateEngine.generate_rds_iam_auth_token(
                                     creds.host, creds.port, creds.user
                                 )
                log.debug("Updated DBCreds with DB token as password")
                creds.optargs.update({"sslmode": "require"})
            else:
                log.debug("Running locally, extracting DB password from environment variables")
                creds.password = getenv("POSTGRES_PASSWORD", "postgres")
                log.debug("Updated DBCreds with envvar as password")
                creds.optargs.update({"sslmode": "disable"})

            for key, value in creds.dict().items():
                if value is None:
                    log.error(f"Missing connection details value: {key}")
                    raise ValueError(f"Missing connection details value: {key}")
            return creds
        except Exception as e:
            log.error("Failed to get connection details for database")
            raise e

    @staticmethod
    def get_engine():
        """Get the database engine

        Returns:
            engine: Database engine
        """
        engine = None
        creds = CreateEngine.get_credentials()
        try:
            engine = create_engine(CreateEngine.generate_connection_string(**creds.dict()),
                pool_pre_ping=True,
                connect_args={
                    "keepalives": 1,
                    "keepalives_idle": 30,
                    "keepalives_interval": 10,
                    "keepalives_count": 5,
                },
            )
            connection = engine.connect()
            log.info("Connection to PostgreSQL DB successful")
            connection.close()
        except Exception as e:
            log.error(f"The error '{e}' occurred")
            raise e
        return engine


class AutoMappingModels:
    def __init__(self):
        self.engine = CreateEngine.get_engine()
        self.Base = automap_base()
        self.Base.prepare(autoload_with=self.engine)
        self.PDBRDRegistration = self.Base.classes.pdbrd_registration
        self.OTCOperator = self.Base.classes.otc_operator
        self.OTCLicence = self.Base.classes.otc_licence
        self.BODSDataCatalogue = self.Base.classes.bods_data_catalogue
        self.PDBRDGroup = self.Base.classes.pdbrd_group
        self.PDBRDReport = self.Base.classes.pdbrd_report
        self.PDBRDStage = self.Base.classes.pdbrd_stage
        self.PDBRDUser = self.Base.classes.pdbrd_user
        self.OTCLicence.__repr__ = (
            lambda self: f"<OTCLicence(licence_number='{self.licence_number}', licence_status='{self.licence_status}')>"
        )
        self.OTCOperator.__repr__ = (
            lambda self: f"<OTCOperator(operator_name='{self.operator_name}')>"
        )
        self.PDBRDRegistration.__repr__ = (
            lambda self: f"<PDBRDRegistration(route_number='{self.route_number}', route_description='{self.route_description}', variation_number='{self.variation_number}', start_point='{self.start_point}', finish_point='{self.finish_point}', via='{self.via}', subsidised='{self.subsidised}', subsidy_detail='{self.subsidy_detail}', is_short_notice='{self.is_short_notice}', received_date='{self.received_date}', granted_date='{self.granted_date}', effective_date='{self.effective_date}', end_date='{self.end_date}', otc_operator_id='{self.otc_operator_id}', bus_service_type_id='{self.bus_service_type_id}', bus_service_type_description='{self.bus_service_type_description}', registration_number='{self.registration_number}', traffic_area_id='{self.traffic_area_id}', application_type='{self.application_type}', publication_text='{self.publication_text}', other_details='{self.other_details}')>"
        )
        self.BODSDataCatalogue.__repr__ = (
            lambda self: f"<BODSDataCatalogue(id='{self.id}', xml_service_code='{self.xml_service_code}', variation_number='{self.variation_number}', service_type_description='{self.service_type_description}', published_status='{self.published_status}', requires_attention='{self.requires_attention}', timeliness_status='{self.timeliness_status}')>"
        )
        self.PDBRDGroup.__repr__ = (
            lambda self: f"<PDBRDGroup(local_auth='{self.local_auth}')>"
        )
        self.PDBRDReport.__repr__ = (
            lambda self: f"<PDBRDReport(id='{self.id}', report_id='{self.report_id}', group_id='{self.user_id}', report='{self.report}')>"
        )
        self.PDBRDStage.__repr__ = (
            lambda self: f"<PDBRDStage(id='{self.id}', stage_id='{self.stage_id}', stage_user='{self.stage_user}', created_at='{self.created_at}')>"
        )
        self.PDBRDUser.__repr__ = (
            lambda self: f"<PDBRDUser(id='{self.id}', user_id='{self.user_name}', group_id='{self.group_id}')>"
        )

    def get_tables(self):
        return {
            "PDBRDRegistration": self.PDBRDRegistration,
            "OTCOperator": self.OTCOperator,
            "OTCLicence": self.OTCLicence,
            "PDBRDGroup": self.PDBRDGroup,
            "PDBRDReport": self.PDBRDReport,
            "BODSDataCatalogue": self.BODSDataCatalogue,
            "PDBRDStage": self.PDBRDStage,
            "PDBRDUser": self.PDBRDUser,
        }


class DBGroup:
    def __init__(self, models, session):
        self.models = models
        self.session = session

    def get_or_create_group(self, group_name: str):
        """Check if the user exists in the database, if not, add the user

        Args:
            user (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        models = self.models
        session = self.session
        PDBRDGroup = models.PDBRDGroup
        try:
            # check if user in db first:
            group = self.get_group(group_name)
            if group:
                return group
            # Add the user
            group = PDBRDGroup(local_auth=group_name)
            session.add(group)
            session.commit()
            return group  # Return the ID of the inserted record
        except Exception as e:
            log.error(f"Error: {e}")
            session.rollback()

    def get_or_create_user(self, user_name: str, group_name: str):
        """Check if the user exists in the database, if not, add the user

        Args:
            user (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        models = self.models
        session = self.session
        PDBRDUser = models.PDBRDUser
        try:
            # check if user in db first:
            user = self.get_user(user_name, group_name)
            if user:
                return user
            # Add the user
            group = self.get_or_create_group(group_name)
            user = PDBRDUser(user_name=user_name, group_id=group.id)
            session.add(user)
            session.commit()
            return user  # Return the ID of the inserted record
        except Exception as e:
            log.error(f"Error: {e}")
            session.rollback()

    def get_group(self, group_name: str, raise_exception: bool = False):
        session = self.session
        PDBRDGroup = self.models.PDBRDGroup
        group = (
            session.query(PDBRDGroup)
            .filter(PDBRDGroup.local_auth == group_name)
            .one_or_none()
        )
        if group:
            return group
        if raise_exception:
            raise GroupIsNotFound(f"Group: {group_name} not found")

    def get_user(self, user_name: str, group_name: str):
        session = self.session
        PDBRDUser = self.models.PDBRDUser
        PDBGroup = self.models.PDBRDGroup
        user = (
            session.query(PDBRDUser)
            .join(PDBGroup, PDBGroup.id == PDBRDUser.group_id)
            .filter(PDBGroup.local_auth == group_name)
            .filter(PDBRDUser.user_name == user_name)
            .one_or_none()
        )
        return user


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
                session.query(Model)
                .filter(getattr(Model, column_name) == value)
                .first()
            )
            return existing_record.id
    except Exception as e:
        log.error(f"Error: {e}")
        session.rollback()
        return None


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
        licence_record_id = add_or_get_record(
            "licence_number", licence_number, session, OTCLicence, licence_record
        )
        return licence_record_id

    @classmethod
    def upsert_record_to_pdbrd_registration_table(
        cls,
        record: Registration,
        operator_record_id: int,
        licence_record_id: int,
        session: Session,
        PDBRDRegistration: Table,
        group_id: int,
    ):
        """Add or update the record to the PDBRDRegistration table

        Args:
            record (Registration):
            operator_record_id (int):
            licence_record_id (int):
            session (Session):
            PDBRDRegistration (Table): Target table

        Raises:
            RecordIsAlreadyExist: If the record already exists in the database
        """
        # Add or update the record to the PDBRDRegistration table
        # case 1: Record already exists in the database
        existing_record = (
            session.query(PDBRDRegistration)
            .filter(
                PDBRDRegistration.registration_number == record.registration_number,
                PDBRDRegistration.otc_operator_id == operator_record_id,
                PDBRDRegistration.variation_number == record.variation_number,
                PDBRDRegistration.group_id == group_id,
                PDBRDRegistration.route_number == record.route_number,
            )
            .one_or_none()
        )

        if existing_record:
            record_dict = record.model_dump()
            existing_record_dict = existing_record.__dict__
            # Add the user id to the record
            record_dict.update({"group_id": group_id})
            if common_keys_comparsion(record_dict, existing_record_dict):
                raise RecordIsAlreadyExist("Record already exists with the same fields")

        else:
            # case 2: Record does not exist, create a new record
            pdbrd_registration_record = PDBRDRegistration(
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
                group_id=group_id,
                pdbrd_stage_id=None,
            )
            session.add(pdbrd_registration_record)
            session.commit()
            log.debug(f"New PDBRD registration record: {pdbrd_registration_record.id}")


def send_to_db(
    records: List[Registration], group_name=None, user_name=None, report_id=None
):
    # validated_records: List[Registration] = MockData.mock_user_csv_record()
    models = AutoMappingModels() 
    engine = models.engine
    tables = models.get_tables()
    OTCOperator = tables["OTCOperator"]
    OTCLicence = tables["OTCLicence"]
    PDBRDRegistration = tables["PDBRDRegistration"]
    PDBRDUser = tables["PDBRDUser"]
    # Check if the licence number exists in the OTC database
    # validated_records = validate_licence_number_existence(validated_records)
    db_invalid_insertion = []
    already_exists_records = {}
    belongs_to_another_user = {}

    # Add or create the group
    session = Session(engine)
    PDBRDUser = DBGroup(models, session).get_or_create_user(user_name, group_name)
    group_id = PDBRDUser.group_id
    # add record to the stage table
    # PDBRDStage_record = PDBRDStage(stage_user=PDBRDUser.id, stage_id=report_id)
    # session.add(PDBRDStage_record)
    # session.commit()
    # PDBRDStage_id = PDBRDStage_record.id
    # session.close()

    for idx, record_and_licence in records["valid_records"].items():
        try:
            # Create a new session
            session = Session(engine)
            # Prepare operator object and added to the database
            record, licence = record_and_licence
            OTCOperator_record = OTCOperator(
                operator_name=licence.operator_details.operator_name,
            )

            # Add or fetch the operator id from the database
            operator_record_id = DBManager.fetch_operator_record(
                licence.operator_details.operator_name,
                session,
                OTCOperator,
                OTCOperator_record,
            )

            # Prepare licence object and added to the database
            OTCLicence_record = OTCLicence(
                licence_number=licence.licence_details.licence_number,
                licence_status=licence.licence_details.licence_status,
            )

            # Add or fetch the licence id from the database
            licence_record_id = DBManager.fetch_licence_record(
                licence.licence_details.licence_number,
                session,
                OTCLicence,
                OTCLicence_record,
            )

            # Add the record to the PDBRDRegistration table
            DBManager.upsert_record_to_pdbrd_registration_table(
                record,
                operator_record_id,
                licence_record_id,
                session,
                PDBRDRegistration,
                group_id,
            )
        except RecordIsAlreadyExist:
            already_exists_records.update(
                {idx: [{"Duplicated Record": "Record already exists in the database"}]}
            )
            db_invalid_insertion.append(idx)
        except RecordBelongsToAnotherUser:
            belongs_to_another_user.update(
                {
                    idx: [
                        {"RecordBelongsToAnotherUser": "Record belongs to another user"}
                    ]
                }
            )
            db_invalid_insertion.append(idx)
            session.commit()
        except Exception as e:
            log.error(f"Error: {e}")
            session.rollback()
        finally:
            session.close()
    # Remove records from the valid_records dictionary that were not added to the database
    for idx in db_invalid_insertion:
        del records["valid_records"][f"{idx}"]
    log.info(f"already_exists_records: {already_exists_records}")
    if len(already_exists_records) > 0:
        records["invalid_records"].append(
            {"records": already_exists_records, "description": "Record already exists"}
        )
    if len(belongs_to_another_user) > 0:
        records["invalid_records"].append(
            {
                "records": belongs_to_another_user,
                "description": "Record belongs to another user",
            }
        )
