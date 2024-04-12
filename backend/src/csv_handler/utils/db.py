import json
from os import getenv
from sqlalchemy import create_engine, func, select, Table, case, desc, or_, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, Query
from sys import exit
from typing import List
from .aws import get_secret
from .csv_validator import Registration
from .logger import console, log
from .pydant_model import AuthenticatedEntity, DBCreds, SearchQuery
from .exceptions import (
    RecordIsAlreadyExist,
    LimitExceeded,
    LimitIsNotSet,
    GroupIsNotFound,
    RecordBelongsToAnotherUser,
)
from .data import common_keys_comparsion
from central_config.env import PROJECT_ENV


class CreateEngine:
    @staticmethod
    def get_db_creds():
        creds = None

        try:
            if PROJECT_ENV != "local":
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
        self.PDBRDRegistration = self.Base.classes.pdbrd_registration
        self.OTCOperator = self.Base.classes.otc_operator
        self.OTCLicence = self.Base.classes.otc_licence
        self.BODSDataCatalogue = self.Base.classes.bods_data_catalogue
        self.PDBRDGroup = self.Base.classes.pdbrd_group
        self.PDBRDReport = self.Base.classes.pdbrd_report
        self.PDBRDStage = self.Base.classes.pdbrd_stage
        self.OTCLicence.__repr__ = (
            lambda self: f"<OTCLicence(licence_number='{self.licence_number}', licence_status='{self.licence_status}, otc_licence_id={self.otc_licence_id}')>"
        )
        self.OTCOperator.__repr__ = (
            lambda self: f"<OTCOperator(operator_name='{self.operator_name}', operator_id='{self.otc_operator_id}')>"
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
            lambda self: f"<PDBRDReport(id='{self.id}', report_id='{self.report_id}', group_id='{self.group_id}', report='{self.report}')>"
        )
        self.PDBRDStage.__repr__ = (
            lambda self: f"<PDBRDStage(id='{self.id}', stage_id='{self.stage_id}', stage_user='{self.stage_user}', created_at='{self.created_at}')>"
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
        }


def add_filter_to_query(query: Query, column, value, strict_mode: bool = False):
    if strict_mode:
        return query.filter(column == value)

    return query.filter(column.like(f"%{value}%"))


def initiate_db_variables():
    models = AutoMappingModels()
    engine = models.engine
    session = Session(engine)
    return models, session


class DBGroup:
    def __init__(self, models, session):
        self.models = models
        self.session = session

    def get_or_create_user(self, group_name:str):
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
            session.close()
            return group  # Return the ID of the inserted record
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
        PDBRDGroup: Table,
        PDBRDStage_id: int
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
                PDBRDRegistration.group_id == PDBRDGroup.id,
            )
            .one_or_none()
        )

        if existing_record:
            record_dict = record.model_dump()
            existing_record_dict = existing_record.__dict__
            # Add the user id to the record
            record_dict.update({"group_id": PDBRDGroup.id})
            if common_keys_comparsion(record_dict, existing_record_dict):
                # case 1.1: Check if all the fields are the same
                # All fields are the same, reject with an error
                # log.debug(
                #     f"Record already exists with the same fields: {existing_record.id}"
                # )
                raise RecordIsAlreadyExist("Record already exists with the same fields")

            # # case 1.2: Not all fields are the same, update the record
            # existing_record.route_number = record.route_number
            # existing_record.route_description = record.route_description
            # existing_record.variation_number = record.variation_number
            # existing_record.start_point = record.start_point
            # existing_record.finish_point = record.finish_point
            # existing_record.via = record.via
            # existing_record.subsidised = record.subsidised
            # existing_record.subsidy_detail = record.subsidy_detail
            # existing_record.is_short_notice = record.is_short_notice
            # existing_record.received_date = record.received_date
            # existing_record.granted_date = record.granted_date
            # existing_record.effective_date = record.effective_date
            # existing_record.end_date = record.end_date
            # existing_record.bus_service_type_id = record.bus_service_type_id
            # existing_record.bus_service_type_description = (
            #     record.bus_service_type_description
            # )
            # existing_record.traffic_area_id = record.traffic_area_id
            # existing_record.application_type = record.application_type
            # existing_record.publication_text = record.publication_text
            # existing_record.other_details = record.other_details
            # existing_record.otc_licence_id = licence_record_id
            # session.commit()
            # log.debug(f"Updated PDBRD registration record: {existing_record.id}")

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
                group_id=PDBRDGroup.id,
                pdbrd_stage_id=PDBRDStage_id
            )
            session.add(pdbrd_registration_record)
            session.commit()
            log.debug(f"New PDBRD registration record: {pdbrd_registration_record.id}")

    @classmethod
    def get_records(
        cls,
        authenticated_entity: AuthenticatedEntity= None,
        exclude_variations: bool = False,
        registration_number: str = None,
        operator_name: str = None,
        route_number: str = None,
        license_number: str = None,
        limit: int | None = None,
        page: int | None = None,
        strict_mode: bool = False,
    ) -> List[dict]:
        """Get records from the database based on the search query

        Args:
            exclude_variations (bool, optional): Defaults to False.
            registration_number (str, optional): Defaults to None.
            operator_name (str, optional): Defaults to None.
            route_number (str, optional): Defaults to None.
            license_number (str, optional): Defaults to None.
            limit (int | None, optional): Defaults to None.
            page (int | None, optional): Defaults to None.
            strict_mode (bool, optional): Defaults to False.

        Raises:
            LimitIsNotSet: If the limit is not set when the page is provided
            LimitExceeded: If the page number exceeds the total number of records

        Returns:
            [dict]: List of records each as a dictionary
        """
        models, session = initiate_db_variables()
        PDBRDRegistration = models.PDBRDRegistration
        OTCOperator = models.OTCOperator
        OTCLicence = models.OTCLicence
        if authenticated_entity.type == "local_auth":
            PDBRDGroup = DBGroup(models, session).get_group(authenticated_entity.name, raise_exception=True)
        else:
            PDBRDGroup = None
        records = (
            session.query(
                PDBRDRegistration.variation_number.label("variationNumber"),
                PDBRDRegistration.registration_number.label("registrationNumber"),
                OTCOperator.operator_name.label("operatorName"),
                OTCLicence.licence_number.label("licenceNumber"),
                PDBRDRegistration.route_number.label("routeNumber"),
                PDBRDRegistration.start_point.label("startPoint"),
                PDBRDRegistration.finish_point.label("finishPoint"),
                PDBRDRegistration.via.label("via"),
                PDBRDRegistration.subsidised.label("subsidised"),
                PDBRDRegistration.subsidy_detail.label("subsidyDetail"),
                PDBRDRegistration.is_short_notice.label("isShortNotice"),
                PDBRDRegistration.received_date.label("receivedDate"),
                PDBRDRegistration.granted_date.label("grantedDate"),
                PDBRDRegistration.effective_date.label("effectiveDate"),
                PDBRDRegistration.end_date.label("endDate"),
                PDBRDRegistration.bus_service_type_id.label("busServiceTypeId"),
                PDBRDRegistration.bus_service_type_description.label(
                    "busServiceTypeDescription"
                ),
                PDBRDRegistration.traffic_area_id.label("trafficAreaId"),
                PDBRDRegistration.application_type.label("applicationType"),
                PDBRDRegistration.publication_text.label("publicationText"),
            )
            .join(OTCOperator, PDBRDRegistration.otc_operator_id == OTCOperator.id)
            .join(OTCLicence, PDBRDRegistration.otc_licence_id == OTCLicence.id)
        )
        # If EGroup is not None, filter the records by the group
        # Otherwise, get all the records
        if PDBRDGroup:
            records = records.filter(PDBRDRegistration.group_id == PDBRDGroup.id)

        if exclude_variations:
            latest_ids = (
                select(func.max(PDBRDRegistration.id))
                .group_by(
                    PDBRDRegistration.registration_number,
                    PDBRDRegistration.otc_operator_id,
                    PDBRDRegistration.group_id,
                )
            )
            if PDBRDGroup:
                latest_ids = latest_ids.filter(PDBRDRegistration.group_id == PDBRDGroup.id).subquery()
            else:
                latest_ids = latest_ids.subquery()
            records = records.filter(
                PDBRDRegistration.id.in_(select(latest_ids))
            )

        if license_number:
            records = add_filter_to_query(
                records, OTCLicence.licence_number, license_number, strict_mode
            )

        if registration_number:
            records = add_filter_to_query(
                records,
                PDBRDRegistration.registration_number,
                registration_number,
                strict_mode,
            )

        if operator_name:
            records = add_filter_to_query(
                records, OTCOperator.operator_name, operator_name, strict_mode
            )

        if route_number:
            records = add_filter_to_query(
                records, PDBRDRegistration.route_number, route_number, strict_mode
            )

        if page:
            cls.record_count = records.count()
            if limit is None:
                raise LimitIsNotSet("Limit must be provided when page is provided")
            offset = (page - 1) * limit
            if offset < records.count():
                records = records.offset(offset)
            else:
                raise LimitExceeded("Page number exceeds the total number of records")

        if limit:
            records = records.limit(limit)

        return [rec._asdict() for rec in records.all()]

    @classmethod
    def construct_next_page_url(
        cls, search_query: SearchQuery, host: str, path: str
    ) -> str:
        """Construct the next page url
        Args:
            search_query (SearchQuery): Search query object from the request
            host (str): Host
            path (str): Path

        Returns:
           NextPage (str) : URL for the next page
        """
        if search_query.page is None:
            return
        if search_query.limit is None:
            return
        if cls.record_count is None:
            return
        # Calculate the next page
        search_query.page += 1
        if search_query.page * search_query.limit > cls.record_count:
            return
        search_params = search_query.model_dump(exclude_none=True, by_alias=True)
        params_str = "&".join([f"{k}={v}" for k, v in search_params.items()])
        return f"{host}{path}?{params_str}"

    @classmethod
    def get_all_records(cls, authenticated_entity: AuthenticatedEntity,latest_only=False):
        models, session = initiate_db_variables()
        PDBRDRegistration = models.PDBRDRegistration
        OTCOperator = models.OTCOperator
        OTCLicence = models.OTCLicence
        BODSDataCatalogue = models.BODSDataCatalogue
        if authenticated_entity.type == "local_auth":
            PDBRDGroup = DBGroup(models, session).get_group(authenticated_entity.name, raise_exception=True)
        else:
            PDBRDGroup = None
        if latest_only:
            subquery_q1 = (
                session.query(
                    PDBRDRegistration.registration_number,
                    func.max(PDBRDRegistration.variation_number).label("max_variation_number")
                ).filter(PDBRDRegistration.pdbrd_stage_id.is_(None))
                .group_by(PDBRDRegistration.registration_number)
                .subquery()
            )

            subquery_q2 = (
                session.query(PDBRDRegistration.id)
                .join(subquery_q1, and_(
                    PDBRDRegistration.registration_number == subquery_q1.c.registration_number,
                    PDBRDRegistration.variation_number == subquery_q1.c.max_variation_number
                ))
            ).subquery()



        records = (
            session.query(
                PDBRDRegistration.registration_number.label("registrationNumber"),
                PDBRDRegistration.route_number.label("routeNumber"),
                PDBRDRegistration.route_description.label("routeDescription"),
                PDBRDRegistration.variation_number.label("variationNumber"),
                PDBRDRegistration.start_point.label("startPoint"),
                PDBRDRegistration.finish_point.label("finishPoint"),
                PDBRDRegistration.via.label("via"),
                PDBRDRegistration.subsidised.label("subsidised"),
                PDBRDRegistration.subsidy_detail.label("subsidyDetail"),
                PDBRDRegistration.is_short_notice.label("isShortNotice"),
                PDBRDRegistration.received_date.label("receivedDate"),
                PDBRDRegistration.granted_date.label("grantedDate"),
                PDBRDRegistration.effective_date.label("effectiveDate"),
                PDBRDRegistration.end_date.label("endDate"),
                PDBRDRegistration.bus_service_type_id.label("busServiceTypeId"),
                PDBRDRegistration.bus_service_type_description.label(
                    "busServiceTypeDescription"
                ),
                PDBRDRegistration.traffic_area_id.label("trafficAreaId"),
                PDBRDRegistration.application_type.label("applicationType"),
                PDBRDRegistration.publication_text.label("publicationText"),
                OTCOperator.operator_name.label("operatorName"),
                OTCLicence.licence_number.label("licenceNumber"),
                OTCLicence.licence_status.label("licenceStatus"),
                BODSDataCatalogue.requires_attention,
                BODSDataCatalogue.timeliness_status,
            )
            .outerjoin(BODSDataCatalogue, BODSDataCatalogue.xml_service_code == PDBRDRegistration.registration_number)
            .filter(PDBRDRegistration.otc_operator_id == OTCOperator.id)
            .filter(PDBRDRegistration.pdbrd_stage_id.is_(None))
            .filter(PDBRDRegistration.otc_licence_id == OTCLicence.id)
            # .filter(
            #     PDBRDRegistration.registration_number == BODSDataCatalogue.xml_service_code
            # )
        )
        if latest_only:
            records = records.filter(PDBRDRegistration.id.in_(subquery_q2))

        if PDBRDGroup:
            records = records.filter(PDBRDRegistration.group_id == PDBRDGroup.id)
        return [rec._asdict() for rec in records.all()]

    @classmethod
    def get_record_required_attention_percentage(cls, authenticated_entity: AuthenticatedEntity = None):
        models, session = initiate_db_variables()
        PDBRDRegistration = models.PDBRDRegistration
        OTCOperator = models.OTCOperator
        OTCLicence = models.OTCLicence
        BODSDataCatalogue = models.BODSDataCatalogue
        if authenticated_entity.type == "local_auth":
            PDBRDGroup = DBGroup(models, session).get_group(authenticated_entity.name, raise_exception=True)
        else:
            PDBRDGroup = None

        subquery_q1 = (
            session.query(
                PDBRDRegistration.registration_number,
                func.max(PDBRDRegistration.variation_number).label("max_variation_number")
            )
            .filter(PDBRDRegistration.pdbrd_stage_id.is_(None))
            .group_by(PDBRDRegistration.registration_number)
            .subquery()
        )
        subquery_q2 = (
            session.query(PDBRDRegistration.id)
            .join(subquery_q1, and_(
                PDBRDRegistration.registration_number == subquery_q1.c.registration_number,
                PDBRDRegistration.variation_number == subquery_q1.c.max_variation_number
            ))
        ).subquery()


        subquery_q3 = (
            session.query(
                func.count(PDBRDRegistration.registration_number).label("count"),
                OTCLicence.licence_number,
                BODSDataCatalogue.requires_attention,
                OTCOperator.operator_name,
                OTCLicence.licence_status,
            )
            .join(OTCLicence, OTCLicence.id == PDBRDRegistration.otc_licence_id)
            .outerjoin(
                BODSDataCatalogue,
                PDBRDRegistration.registration_number
                == BODSDataCatalogue.xml_service_code,
            )
            .join(OTCOperator, OTCOperator.id == PDBRDRegistration.otc_operator_id)
            .filter(PDBRDRegistration.group_id == PDBRDGroup.id)
            .filter(PDBRDRegistration.id.in_(subquery_q2))
            .group_by(
                OTCLicence.licence_number,
                OTCOperator.operator_name,
                BODSDataCatalogue.requires_attention,
                OTCLicence.licence_status,
            )          
        )
        if PDBRDGroup:
            subquery_q3 = subquery_q3.filter(PDBRDRegistration.group_id == PDBRDGroup.id).subquery()
        else:
            subquery_q3 = subquery_q3.subquery()

        query = (
            session.query(
            subquery_q3.c.licence_number,
            subquery_q3.c.operator_name,
            subquery_q3.c.licence_status,
            func.round(
                (
                100.0
                * func.sum(
                    case(
                    (
                        (
                        or_(subquery_q3.c.requires_attention.is_(True), subquery_q3.c.requires_attention.is_(None)),
                        subquery_q3.c.count,
                        )
                    ),
                    else_=0,
                    )
                )
                / func.sum(subquery_q3.c.count)
                ),
                2,
            ).label("requires_attention"),
            func.sum(subquery_q3.c.count).label("total_services"),
            func.sum(case(
                (
                   (
                       subquery_q3.c.requires_attention.is_(None),
                       subquery_q3.c.count,
                   )
                ),
                else_=0
            )).label("Registrations_not_in_BODS")
            )
            .group_by(
            subquery_q3.c.licence_number,
            subquery_q3.c.operator_name,
            subquery_q3.c.licence_status,
            )
            .order_by(desc("total_services"))
        )
        return [rec._asdict() for rec in query.all()]

    @classmethod
    def get_report_then_delete_it_from_db(cls, authenticated_entity: AuthenticatedEntity, report_id: str):
        models, session = initiate_db_variables()
        PDBRDReport = models.PDBRDReport
        PDBRDGroup = models.PDBRDGroup
        if authenticated_entity.type == "local_auth":
            PDBRDGroup = DBGroup(models, session).get_group(authenticated_entity.name, raise_exception=False)
        if not PDBRDGroup:
            return None
        report = (
            session.query(PDBRDReport)
            .filter(PDBRDReport.report_id == report_id)
            .filter(PDBRDReport.group_id == PDBRDGroup.id)
            .one_or_none()
        )
        if report:
            # Delete report from db:
            session.delete(report)
            session.commit()
            return report.report
        return None

    @classmethod
    def get_staged_records(cls, authenticated_entity: AuthenticatedEntity, stage_id: str=None):
        models, session = initiate_db_variables()
        PDBRDStage = models.PDBRDStage
        PDBRDGroup = models.PDBRDGroup
        PDBRDLicence = models.OTCLicence
        PDBRDOperator = models.OTCOperator
        PDBRDRegistration = models.PDBRDRegistration
        if authenticated_entity.type == "local_auth":
            PDBRDGroup = DBGroup(models, session).get_group(authenticated_entity.name, raise_exception=True)
        if not PDBRDGroup:
            return None
        staged_process = (
            session.query(PDBRDStage.id).filter(PDBRDStage.stage_id == stage_id).subquery()
        )

        staged_records = (
            session.query(PDBRDRegistration.registration_number, PDBRDLicence.licence_number, PDBRDOperator.operator_name)
            .filter(PDBRDRegistration.pdbrd_stage_id == select(staged_process.c.id))
            .filter(PDBRDRegistration.otc_licence_id == PDBRDLicence.id)
            .filter(PDBRDRegistration.otc_operator_id == PDBRDOperator.id)
            
        )
        console.log(staged_records)

        return [rec._asdict() for rec in staged_records.all()]

    @classmethod
    def commit_staged_records(cls, authenticated_entity: AuthenticatedEntity, stage_id: str, commit: bool = True):
        models, session = initiate_db_variables()
        PDBRDStage = models.PDBRDStage
        PDBRDGroup = models.PDBRDGroup
        PDBRDRegistration = models.PDBRDRegistration
        if authenticated_entity.type == "local_auth":
            PDBRDGroup = DBGroup(models, session).get_group(authenticated_entity.name, raise_exception=True)
        if not PDBRDGroup:
            return None

        try:
            if not  commit:
                # Get the staged process id
                staged_process_id = (
                    session.query(PDBRDStage.id)
                    .filter(PDBRDStage.stage_id == stage_id)
                    .filter(PDBRDStage.stage_user == PDBRDGroup.id)
                )
                staged_process_subquery = staged_process_id.subquery()
                staged_records = (
                    session.query(PDBRDRegistration)
                    .filter(PDBRDRegistration.pdbrd_stage_id == select(staged_process_subquery).scalar_subquery())
                )
                staged_records.delete(synchronize_session=False)

            # Get the staged process
            staged_process = (
                    session.query(PDBRDStage)
                    .filter(PDBRDStage.stage_id == stage_id)
                    .filter(PDBRDStage.stage_user == PDBRDGroup.id)
                )
            # Delete the staged process
            deleted_count = staged_process.delete(synchronize_session=False)
            session.commit()
            session.close()
            if deleted_count > 0:
                return True
            return False
        except Exception as e:
            console.log(e)
            session.rollback()
            session.close()


    @classmethod
    def commit_discard_changes(cls, session: Session, commit: bool = False):
        if commit:
            session.commit()
        else:
            session.rollback()
        session.close()

    @classmethod
    def get_staged_process(cls, authenticated_entity: AuthenticatedEntity):
        models, session = initiate_db_variables()
        PDBRDStage = models.PDBRDStage
        PDBRDGroup = models.PDBRDGroup
        if authenticated_entity.type == "local_auth":
            PDBRDGroup = DBGroup(models, session).get_group(authenticated_entity.name, raise_exception=False)
        if not PDBRDGroup:
            return None
        staged_process = (
            session.query(PDBRDStage.stage_id, PDBRDStage.created_at)
            .filter(PDBRDStage.stage_user == PDBRDGroup.id)
        )
        console.log(staged_process.all())
        return [rec._asdict() for rec in staged_process.all()]


def send_to_db(records: List[Registration], group_name = None, report_id = None):
    # validated_records: List[Registration] = MockData.mock_user_csv_record()
    models = AutoMappingModels()
    engine = models.engine
    tables = models.get_tables()
    OTCOperator = tables["OTCOperator"]
    OTCLicence = tables["OTCLicence"]
    PDBRDRegistration = tables["PDBRDRegistration"]
    PDBRDStage = tables["PDBRDStage"]
    # Check if the licence number exists in the OTC database
    # validated_records = validate_licence_number_existence(validated_records)
    db_invalid_insertion = []
    already_exists_records = {}
    belongs_to_another_user = {}



    # Add or create the user
    PDBRDGroup = DBGroup(models, Session(engine)).get_or_create_user(group_name)
    console.log(PDBRDGroup)
    console.log(PDBRDGroup.id)
    # Initiate a new stage for the records
    # stage = PDBRDStage(stage_user=PDBRDGroup.id,stage_id=report_id)
    # add record to the stage table
    session = Session(engine)
    PDBRDStage_record = PDBRDStage(stage_user=PDBRDGroup.id, stage_id=report_id)
    session.add(PDBRDStage_record)
    session.commit()
    PDBRDStage_id = PDBRDStage_record.id
    console.log(PDBRDStage_id)
    session.close()

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





            # Add the record to the PDBRDRegistration table
            DBManager.upsert_record_to_pdbrd_registration_table(
                record,
                operator_record_id,
                licence_record_id,
                session,
                PDBRDRegistration,
                PDBRDGroup,
                PDBRDStage_id
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
        except Exception:
            console.print_exception(show_locals=False)
            session.rollback()
        finally:
            session.close()
    # Remove records from the valid_records dictionary that were not added to the database
    for idx in db_invalid_insertion:
        del records["valid_records"][f"{idx}"]
    if len(already_exists_records) > 0:
        records["invalid_records"].append(
            {"records": already_exists_records, "description": "Record already exists"}
        )
    if len(belongs_to_another_user) > 0:
        records["invalid_records"].append(
            {"records": belongs_to_another_user, "description": "Record belongs to another user"}
        )
    # console.log(records)
    # if len(records["valid_records"]) == 0:
    #     ## Delete the staged process
    #     session = Session(engine)
    #     staged_process = (
    #         session.query(PDBRDStage)
    #         .filter(PDBRDStage.stage_id == PDBRDStage_id)
    #         .filter(PDBRDStage.stage_user == PDBRDGroup.id)
    #     )
    #     staged_process.delete()
    #     session.commit()
    #     session.close()


def send_report_to_db(report: dict, group_name: str, report_id: str):
    models, session = initiate_db_variables()

    PDBRDGroup = DBGroup(models, session).get_or_create_user(group_name)
    PDBRDReport = models.PDBRDReport
    report_record = PDBRDReport(
        report_id=report_id, group_id=PDBRDGroup.id, report=report
    )
    session.add(report_record)
    session.commit()
    session.close()