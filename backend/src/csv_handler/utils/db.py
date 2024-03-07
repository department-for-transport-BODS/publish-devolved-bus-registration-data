from ctypes import Union
import json
from os import getenv
from sqlalchemy import create_engine, select, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, Query
from sys import exit
from typing import List
from .aws import get_secret
from .csv_validator import Registration
from .logger import console, log
from .pydant_model import DBCreds
from sqlalchemy.exc import NoResultFound, IntegrityError
from .exceptions import RecordIsAlreadyExist
from sqlalchemy import desc, func


class CreateEngine:
    @staticmethod
    def get_db_creds():
        try:
            if getenv("PROJECT_ENV", "localdev") != "localdev":
                secret = get_secret(getenv("POSTGRES_CREDENTIALS"))
                creds = DBCreds(**json.loads(secret["text_secret_data"]))
            else:
                creds = DBCreds(
                    **{
                        "username": getenv("POSTGRES_USER", "postgres"),
                        "password": getenv("POSTGRES_PASSWORD", "postgres"),
                    }
                )
        except Exception as e:
            print(f"The error '{e}' occurred")
            exit(1)
        return creds

    @staticmethod
    def get_engine():
        engine = None
        creds = CreateEngine.get_db_creds()
        try:
            engine = create_engine(
                f"postgresql://{creds.PG_USER}:{creds.PG_PASSWORD}@{creds.PG_HOST}:{creds.PG_PORT}/{creds.PG_DB}"
            )
            connection = engine.connect()
            print("Connection to PostgreSQL DB successful")
            connection.close()
        except Exception as e:
            print(f"The error '{e}' occurred")
            exit(1)
        return engine


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


class AutoMappingModels:
    def __init__(self):
        self.engine = CreateEngine.get_engine()
        self.Base = automap_base()
        self.Base.prepare(autoload_with=self.engine)
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
        def record_exists(cls, session: Session, Model, **kwargs) -> bool:
            try:
                query = session.query(Model).filter_by(**kwargs)
                query.one()
                return True
            except NoResultFound:
                return False
        def upsert_record_to_ep_registration_table(
            cls,
            record: Registration,
            operator_record_id: int,
            licence_record_id: int,
            session: Session,
            EPRegistration: Table,
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

            try:
                # check if the record exists
                if cls.record_exists(
                    session,
                    EPRegistration,
                    otc_licence_id=record.otc_licence_id,
                    registration_number=record.registration_number,
                    variation_number=record.variation_number,
                ):
                    # update record
                    session.query(EPRegistration).filter(ep_registration_record.id == EPRegistration.id).update(

                session.add(ep_registration_record)
                session.flush()
                log.debug(f"New EP registration record: {ep_registration_record.id}")
                session.commit()
            except IntegrityError:
                raise RecordIsAlreadyExist("Record already exists in the database")

    @classmethod
    def get_latest_records(cls):
        models = AutoMappingModels()
        session = Session(models.engine)
        EPRegistration = models.EPRegistration
        OTCLicence = models.OTCLicence

        result = session.query(func.max(EPRegistration.id)).group_by(
            EPRegistration.otc_licence_id, EPRegistration.registration_number
        )
        result2 = session.query(
            EPRegistration.variation_number, EPRegistration.registration_number
        ).filter(EPRegistration.id.in_(result))
        result3 = result2.with_entities(
            OTCLicence.licence_number,
            EPRegistration.variation_number,
            EPRegistration.registration_number,
        ).filter(OTCLicence.id == EPRegistration.otc_licence_id)
        from pydantic import BaseModel

        class LatestRecord(BaseModel):
            variation_number: int
            registration_number: str

        # records = [LatestRecord(**row) for row in result]

        # console.log(dir(result2))
        from rich import table
        from typing import Union

        for row in result2:
            console.log(LatestRecord(**row._asdict()))

        class OTC(BaseModel):
            id: int
            licence_number: str
            license_status: str

        class REG(BaseModel):
            variation_number: int
            registration_number: str

        class JointRecord(BaseModel):
            otc_licence: OTC
            ep_registration: REG

        for row in result3:
            dict_row = row._asdict()
            # console.log(row)
            console.log(dict_row)
            console.log(row[0])
            # console.log(otc_table.__dict__)
            # console.log(JointRecord(otc_licence=OTC(**row[0].__dict__), ep_registration=REG(**row[1].__dict__)))
            # console.log(row._asdict())
            # console.log(table1.add_row(row.variation_number, row.registration_number))
        return


def send_to_db(records: List[Registration]):
    """Send the validated records to the database
    Functionality:
        - Check if the licence number exists in the OTC database
        - Prepare operator object and added to the database
        - Prepare licence object and added to the database
        - Add the record to the EPRegistration table
        - Modify the records dictionary to remove records that were not added to the database
        IF a record exists in the ep_registration table
            then its moved to invalid_records with reason "Record is already exist in the database"



    Args:
        records (List[Registration]): List of validated records

    Returns:
        records List: after updating the valid_records and invalid_records
    """
    # validated_records: List[Registration] = MockData.mock_user_csv_record()
    models = AutoMappingModels()
    engine = models.engine
    tables = models.get_tables()
    OTCOperator = tables["OTCOperator"]
    OTCLicence = tables["OTCLicence"]
    EPRegistration = tables["EPRegistration"]
    # Check if the licence number exists in the OTC database
    # validated_records = validate_licence_number_existence(validated_records)
    db_invalid_insertion = []
    for idx, record_and_licence in records["valid_records"].items():
        try:
            # Create a new session
            session = Session(engine)
            # Prepare operator object and added to the database
            record, licence = record_and_licence
            OTCOperator_record = OTCOperator(
                operator_name=licence.operator_details.operator_name,
                otc_operator_id=licence.operator_details.otc_operator_id,
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
                otc_licence_id=licence.licence_details.otc_licence_id,
            )

            # Add or fetch the licence id from the database
            licence_record_id = DBManager.fetch_licence_record(
                licence.licence_details.licence_number,
                session,
                OTCLicence,
                OTCLicence_record,
            )
            log.debug(f"Record with number: {idx} going to db")
            # Add the record to the EPRegistration table
            DBManager.upsert_record_to_ep_registration_table(
                record, operator_record_id, licence_record_id, session, EPRegistration
            )
        except RecordIsAlreadyExist:
            records["invalid_records"].update(
                {
                    idx: [
                        {"Duplicated Record": "Record is already exist in the database"}
                    ]
                }
            )
            db_invalid_insertion.append(idx)
        except Exception as e:
            # console.log(f"Error: {e}")
            # log.error(f"{e}")
            console.print_exception(show_locals=False)
            # console.print_exception(show_locals=False)
            session.rollback()
        finally:
            session.close()
    # Remove records from the valid_records dictionary that were not added to the database
    for idx in db_invalid_insertion:
        del records["valid_records"][f"{idx}"]

    return records

    # def get_latest_records(cls, session: Session, EPRegistration: Table, limit: int) -> List[Registration]:
    #    'add_column',
    #    'add_columns',
    #    'add_entity',
    #    'all',
    #    'allows_lambda',
    #    'apply_labels',
    #    'as_scalar',
    #    'autoflush',
    #    'column_descriptions',
    #    'correlate',
    #    'count',
    #    'cte',
    #    'delete',
    #    'dispatch',
    #    'distinct',
    #    'enable_assertions',
    #    'enable_eagerloads',
    #    'except_',
    #    'except_all',
    #    'execution_options',
    #    'exists',
    #    'filter',
    #    'filter_by',
    #    'first',
    #    'from_statement',
    #    'get',
    #    'get_children',
    #    'get_execution_options',
    #    'get_label_style',
    #    'group_by',
    #    'having',
    #    'instances',
    #    'intersect',
    #    'intersect_all',
    #    'is_delete',
    #    'is_dml',
    #    'is_insert',
    #    'is_select',
    #    'is_single_entity',
    #    'is_text',
    #    'is_update',
    #    'join',
    #    'label',
    #    'lazy_loaded_from',
    #    'limit',
    #    'load_options',
    #    'logger',
    #    'logging_name',
    #    'memoized_attribute',
    #    'memoized_instancemethod',
    #    'merge_result',
    #    'offset',
    #    'one',
    #    'one_or_none',
    #    'only_return_tuples',
    #    'options',
    #    'order_by',
    #    'outerjoin',
    #    'params',
    #    'populate_existing',
    #    'prefix_with',
    #    'reset_joinpoint',
    #    'scalar',
    #    'scalar_subquery',
    #    'select_from',
    #    'selectable',
    #    'session',
    #    'set_label_style',
    #    'slice',
    #    'statement',
    #    'subquery',
    #    'suffix_with',
    #    'supports_execution',
    #    'tuples',
    #    'union',
    #    'union_all',
    #    'update',
    #    'uses_inspection',
    #    'value',
    #    'values',
    #    'where',
    #    'whereclause',
    #    'with_entities',
    #    'with_for_update',
    #    'with_hint',
    #    'with_labels',
    #    'with_parent',
    #    'with_session',
    #    'with_statement_hint',
    #    'with_transformation',
    #    'yield_per'
