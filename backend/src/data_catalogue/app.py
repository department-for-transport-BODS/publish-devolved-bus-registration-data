from csv import DictReader
from io import BytesIO, TextIOWrapper
from os import getenv
from pydantic import BaseModel, Field, field_validator, AliasChoices
from requests import get, Response
from sqlalchemy import create_engine, Column, String, Boolean, Integer, text
from sqlalchemy.orm import declarative_base, Session
from zipfile import ZipFile
import boto3
import logging
import urllib.parse

logging.basicConfig(format="%(levelname)s,%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, getenv("LOG_LEVEL", "INFO")))

ENVIRONMENT = getenv("PROJECT_ENV", "local")
DATA_CATALOGUE_URL = getenv(
    "DATA_CATALOGUE_URL", "https://data.bus-data.dft.gov.uk/catalogue/"
)

Base = declarative_base()


class DBCatalogueEntry(Base):
    __tablename__ = "bods_data_catalogue"
    id = Column(Integer, primary_key=True)
    xml_service_code = Column(String)
    variation_number = Column(Integer)
    service_type_description = Column(String)
    published_status = Column(String)
    timeliness_status = Column(String)
    requires_attention = Column(Boolean)


class CatalogueEntry(BaseModel):
    xml_service_code: str = Field(
        ..., validation_alias=AliasChoices("XML:Service Code", "xml_service_code")
    )
    variation_number: int = Field(
        default=None,
        validation_alias=AliasChoices("OTC:Variation Number", "variation_number"),
    )
    service_type_description: str = Field(
        ...,
        validation_alias=AliasChoices(
            "OTC:Service Type Description", "service_type_description"
        ),
    )
    published_status: str = Field(
        ..., validation_alias=AliasChoices("Published Status", "published_status")
    )
    timeliness_status: str = Field(
        ..., validation_alias=AliasChoices("Timeliness Status", "timeliness_status")
    )
    requires_attention: bool = Field(
        ..., validation_alias=AliasChoices("Requires Attention", "requires_attention")
    )

    @field_validator("xml_service_code", mode="after")
    @classmethod
    def check_alphanumeric(cls, v: str) -> str:
        if isinstance(v, str):
            return v.replace(":", "/")

    @field_validator(
        "service_type_description",
        "published_status",
        "timeliness_status",
        mode="after",
    )
    @classmethod
    def blank_to_none(cls, v: str):
        if v == "":
            return None
        else:
            return v

    @field_validator("variation_number", mode="plain")
    def allow_none(cls, v):
        if isinstance(v, int):
            return v
        elif v == "" or v is None:
            return None
        else:
            try:
                return int(v)
            except Exception:
                raise ValueError(
                    "Must be an int, int-like string, empty string or None"
                )


class TimetableData:
    def __init__(self):
        self.engine = None
        creds = self._get_connection_details()

        self.engine = create_engine(
            self._generate_connection_string(**creds),
            pool_pre_ping=True,
            connect_args={
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )

    def _get_connection_details(self):
        """
        Method to get the connection details for the database from the environment variables
        """
        connection_details = {}
        connection_details["host"] = getenv("POSTGRES_HOST", "postgres")
        connection_details["port"] = getenv("POSTGRES_PORT", "5432")
        connection_details["dbname"] = getenv("POSTGRES_DB", "postgres")
        connection_details["user"] = getenv("POSTGRES_USER", "postgres")

        try:
            if ENVIRONMENT != "local":
                logger.debug("Getting DB token")
                connection_details["password"] = self._generate_rds_iam_auth_token(
                    connection_details["host"],
                    connection_details["port"],
                    connection_details["user"],
                )
                logger.debug("Updated object with DB token as password")
                connection_details["sslmode"] = "require"
            else:
                logger.debug(
                    "Running locally, extracting DB password from environment variables"
                )
                connection_details["password"] = getenv("POSTGRES_PASSWORD", "postgres")
                logger.debug("Updated object with envvar as password")
                connection_details["sslmode"] = "disable"

            for key, value in connection_details.items():
                if value is None:
                    logger.error(f"Missing connection details value: {key}")
                    raise ValueError
            return connection_details
        except Exception as e:
            logger.error("Failed to get connection details for database")
            raise e

    def _generate_connection_string(self, **kwargs) -> str:
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
        for key, value in kwargs.items():
            if key not in ["host", "port", "user", "password", "dbname"] and value:
                other_parts += f"{key}={value}&"

        # Construct the final connection string
        connection_string = (
            f"postgresql+psycopg2://{user_password}{kwargs.get('host', '')}"
        )
        if kwargs.get("port"):
            connection_string += f":{kwargs.get('port')}"
        connection_string += f"/{kwargs.get('dbname', '')}"
        if other_parts:
            connection_string += f"?{other_parts[:-1]}"

        return connection_string

    def _generate_rds_iam_auth_token(self, host, port, username) -> str:
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
                service_name="rds", region_name=getenv("AWS_REGION")
            )
            token = client.generate_db_auth_token(
                DBHostname=host, DBUsername=username, Port=port
            )
            return urllib.parse.quote_plus(token)
        except Exception as e:
            logger.error(f"An error occurred while generating the IAM auth token: {e}")
            return None

    def refresh(self):
        url: str = DATA_CATALOGUE_URL

        try:
            logger.info(f"Attempting to connect to BODS Data Catalogue at {url}")
            req: Response = get(url)
            req.raise_for_status()
            logger.debug(f"Received reponse: {req.status_code}")
        except Exception as error:
            logger.error(f"An error occured: {error}")
            raise error

        try:
            logger.info("Attempting to consume BODS Data Catalogue from zip files")
            with ZipFile(BytesIO(req.content)) as zipfile:
                with zipfile.open("timetables_data_catalogue.csv") as myfile:
                    csv_reader: DictReader = DictReader(TextIOWrapper(myfile))
                    csv_data: list = [row for row in csv_reader]
                    logger.debug(f"Rows in CSV: {len(csv_data)}")
                    validated_data: list = [CatalogueEntry(**row) for row in csv_data]
                    # logger.debug(f"Validated data: {validated_data}")
                    logger.info(
                        f"Validated data successfully. Count: {len(validated_data)}"
                    )
                    with Session(self.engine) as session:
                        logger.info("Deleting existing data in database")
                        session.execute(
                            text("alter sequence bods_data_catalogue_id_seq restart")
                        )
                        session.query(DBCatalogueEntry).delete()
                        for row in validated_data:
                            session.add(DBCatalogueEntry(**row.model_dump()))
                        try:
                            logger.info("Attempting to write new data to the database")
                            session.commit()
                        except Exception as e:
                            session.rollback()
                            raise e

            return csv_data

        except Exception as error:
            logger.error(f"An error occured: {error}")
            raise error


def lambda_handler(event, context):
    logger.info("Starting BODS Data Catalogue refresh")
    data = TimetableData()
    data.refresh()
    logger.info("BODS Data Catalogue refresh successfully completed")
