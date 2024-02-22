from requests import get, Response
from zipfile import ZipFile
from io import BytesIO, TextIOWrapper
from csv import DictReader
from pydantic import BaseModel, Field, field_validator, AliasChoices
from sqlalchemy import create_engine, Column, String, Boolean, Integer, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, Session
from os import getenv

DATA_CATALOGUE_URL = getenv(
    "DATA_CATALOGUE_URL", "https://data.bus-data.dft.gov.uk/catalogue/"
)
POSTGRES_HOST = getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = getenv("POSTGRES_DB", "epp")

Base = declarative_base()

db_url = URL.create(
    drivername="postgresql",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    port=POSTGRES_PORT,
)


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
        self.engine = create_engine(db_url)

    def refresh(self):
        url: str = DATA_CATALOGUE_URL

        try:
            req: Response = get(url)
            req.raise_for_status()
        except Exception as error:
            raise error

        try:
            with ZipFile(BytesIO(req.content)) as zipfile:
                with zipfile.open("timetables_data_catalogue.csv") as myfile:
                    csv_reader: DictReader = DictReader(TextIOWrapper(myfile))
                    csv_data: list = [row for row in csv_reader]
                    validated_data: list = [CatalogueEntry(**row) for row in csv_data]
                    with Session(self.engine) as session:
                        session.execute(
                            text("alter sequence bods_data_catalogue_id_seq restart")
                        )
                        session.query(DBCatalogueEntry).delete()
                        for row in validated_data:
                            session.add(DBCatalogueEntry(**row.model_dump()))
                        try:
                            session.commit()
                        except Exception as e:
                            session.rollback()
                            raise e

            return csv_data

        except Exception as error:
            raise error


def lambda_handler(event, context):
    data = TimetableData()
    data.refresh()
