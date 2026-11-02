import os
from datetime import date
from unittest.mock import Mock, patch
from types import SimpleNamespace
import pytest
from sqlalchemy import Boolean, Column, Date, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

from utils.db import (
    AutoMappingModels,
    DBManager,
    add_or_get_record,
    CreateEngine,
    send_report_to_db,
)

Base = declarative_base()


@pytest.fixture
def catalogue_join_db():
    base = declarative_base()

    class RegistrationModel(base):
        __tablename__ = "pdbrd_registration"
        id = Column(Integer, primary_key=True)
        registration_number = Column(String)
        route_number = Column(String)
        route_description = Column(String)
        variation_number = Column(Integer)
        start_point = Column(String)
        finish_point = Column(String)
        via = Column(String)
        subsidised = Column(String)
        subsidy_detail = Column(String)
        is_short_notice = Column(Boolean)
        received_date = Column(Date)
        granted_date = Column(Date)
        effective_date = Column(Date)
        end_date = Column(Date)
        bus_service_type_id = Column(Integer)
        bus_service_type_description = Column(String)
        traffic_area_id = Column(String)
        application_type = Column(String)
        publication_text = Column(String)
        otc_operator_id = Column(Integer)
        otc_licence_id = Column(Integer)
        pdbrd_stage_id = Column(Integer)
        group_id = Column(Integer)

    class OperatorModel(base):
        __tablename__ = "otc_operator"
        id = Column(Integer, primary_key=True)
        operator_name = Column(String)

    class LicenceModel(base):
        __tablename__ = "otc_licence"
        id = Column(Integer, primary_key=True)
        licence_number = Column(String)
        licence_status = Column(String)

    class CatalogueModel(base):
        __tablename__ = "bods_data_catalogue"
        id = Column(Integer, primary_key=True)
        xml_service_code = Column(String)
        variation_number = Column(Integer)
        requires_attention = Column(Boolean)
        timeliness_status = Column(String)

    models = SimpleNamespace(
        PDBRDRegistration=RegistrationModel,
        OTCOperator=OperatorModel,
        OTCLicence=LicenceModel,
        BODSDataCatalogue=CatalogueModel,
    )
    engine = create_engine("sqlite:///:memory:")
    base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([OperatorModel(id=1), LicenceModel(id=1)])
        session.add_all([
            RegistrationModel(
                registration_number=code,
                route_number=route,
                variation_number=1,
                effective_date=date(2020, 1, 1),
                otc_operator_id=1,
                otc_licence_id=1,
                group_id=1,
            )
            for code, route in [("R1", "1"), ("R1", "2"), ("R2", "3")]
        ])
        session.commit()
        with patch("utils.db.initiate_db_variables", return_value=(models, session)):
            yield models, session
    engine.dispose()


@pytest.mark.parametrize(
    "statuses",
    [
        [(True, "On time"), (True, "On time")],
        [(True, "On time"), (True, "On time"), (False, "On time")],
        [(True, "On time"), (True, "Late"), (True, "Late")],
        [(None, None), (None, None)],
        [(True, None), (True, None), (True, "On time")],
        [(None, "On time"), (None, "On time"), (False, "On time")],
        [],
    ],
)
def test_get_all_records_distinct_catalogue_statuses(catalogue_join_db, statuses):
    models, session = catalogue_join_db
    session.add_all([
        models.BODSDataCatalogue(
            xml_service_code="R1",
            variation_number=variation,
            requires_attention=attention,
            timeliness_status=timeliness,
        )
        for variation, (attention, timeliness) in enumerate(statuses)
    ])
    session.add(models.BODSDataCatalogue(
        xml_service_code="OTHER", requires_attention=False, timeliness_status="Late"
    ))
    session.commit()

    records = DBManager.get_all_records(SimpleNamespace(type="api"), active_only=False)

    expected_statuses = set(statuses) or {(None, None)}
    assert len(records) == 2 * len(expected_statuses) + 1
    for route in ["1", "2"]:
        assert {
            (row["requires_attention"], row["timeliness_status"])
            for row in records
            if row["registrationNumber"] == "R1" and row["routeNumber"] == route
        } == expected_statuses
    unmatched = [row for row in records if row["registrationNumber"] == "R2"]
    assert len(unmatched) == 1
    assert unmatched[0]["requires_attention"] is None
    assert unmatched[0]["timeliness_status"] is None


@pytest.fixture
def mocked_db():
    # Implement your mocked database setup here
    # For example, you can use an in-memory SQLite database
    # and return a session object
    # Make sure to import the necessary modules and classes

    # Example implementation:
    engine = create_engine("sqlite:///:memory:")
    session = Session(engine)
    Base.metadata.create_all(engine)
    yield session
    session.close()


class TestModel(Base):
    __test__ = False
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


def test_add_or_get_record_when_record_does_not_exist(mocked_db):
    session = mocked_db
    record = TestModel(name="Test Record")
    result = add_or_get_record("name", "Test Record", session, TestModel, record)
    assert result == 1  # Assuming the id of the new record is 1


def test_add_or_get_record_when_record_exists(mocked_db):
    session = mocked_db
    existing_record = TestModel(id=1, name="Test Record")
    session.add(existing_record)
    session.commit()

    record = TestModel(name="Test Record")
    result = add_or_get_record("name", "Test Record", session, TestModel, record)
    assert result == 1  # Assuming the id of the existing record is 1


def test_add_or_get_record_with_exception(mocked_db):
    session = mocked_db
    record = TestModel(name="Test Record")
    session.query = Mock(side_effect=Exception("Test Exception"))

    result = add_or_get_record("name", "Test Record", session, TestModel, record)
    assert result is None


class TestAutoMappingModels:
    @pytest.fixture
    def auto_mapping_models(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)

        mock_base = Mock()
        mock_base.classes.pdbrd_registration = TestModel
        mock_base.classes.otc_operator = TestModel
        mock_base.classes.otc_licence = TestModel
        mock_base.classes.bods_data_catalogue = TestModel
        mock_base.classes.pdbrd_group = TestModel
        mock_base.classes.pdbrd_report = TestModel
        mock_base.classes.pdbrd_stage = TestModel
        mock_base.classes.pdbrd_user = TestModel

        with patch("utils.db.CreateEngine.get_engine", return_value=engine), \
             patch("utils.db.automap_base", return_value=mock_base):
            return AutoMappingModels()

    def test_get_tables(self, auto_mapping_models):
        tables = auto_mapping_models.get_tables()
        assert isinstance(tables, dict)
        assert "PDBRDRegistration" in tables
        assert "OTCOperator" in tables
        assert "OTCLicence" in tables
        assert isinstance(
            tables["PDBRDRegistration"], type(auto_mapping_models.PDBRDRegistration)
        )
        assert isinstance(tables["OTCOperator"], type(auto_mapping_models.OTCOperator))
        assert isinstance(tables["OTCLicence"], type(auto_mapping_models.OTCLicence))


class TestDBManager:
    @pytest.fixture
    def mocked_db(self):
        engine = create_engine("sqlite:///test_db_file.csv")
        session = Session(engine)
        Base.metadata.create_all(engine)
        yield session
        session.close()
        # remove the file
        os.remove("test_db_file.csv")

    @patch("utils.db.add_or_get_record", return_value=1)
    def test_fetch_operator_record(self, mocked_db):
        session = mocked_db
        OTCOperator = TestModel
        operator_record = TestModel()
        operator_name = "Test Operator"

        result = DBManager.fetch_operator_record(
            operator_name, session, OTCOperator, operator_record
        )

        assert result == 1

    @patch("utils.db.add_or_get_record", return_value=1)
    def test_fetch_licence_record(self, mocked_db):
        session = mocked_db
        OTCLicence = TestModel
        licence_record = TestModel()
        licence_number = "Test Licence"

        result = DBManager.fetch_licence_record(
            licence_number, session, OTCLicence, licence_record
        )

        assert result == 1


def test_registration_retry_ignores_record_already_written_to_same_stage():
    class RegistrationModel:
        registration_number = "registration_number"
        otc_operator_id = "otc_operator_id"
        variation_number = "variation_number"
        group_id = "group_id"
        route_number = "route_number"

    query = Mock()
    query.filter.return_value = query
    query.one_or_none.return_value = SimpleNamespace(pdbrd_stage_id=7)
    session = Mock()
    session.query.return_value = query
    record = SimpleNamespace(
        registration_number="R1", variation_number=0, route_number="1"
    )

    DBManager.upsert_record_to_pdbrd_registration_table(
        record, 1, 2, session, RegistrationModel, 3, 7
    )

    session.add.assert_not_called()
    session.commit.assert_not_called()


def test_send_report_to_db_updates_existing_report_for_retry():
    report_model = Mock()
    report_model.report_id = "report_id"
    report_model.user_id = "user_id"

    existing_report = SimpleNamespace(report={"old": True})
    session = Mock()
    session.query.return_value.filter.return_value.one_or_none.return_value = (
        existing_report
    )
    models = SimpleNamespace(PDBRDReport=report_model)
    user = SimpleNamespace(id=5)

    with patch("utils.db.initiate_db_variables", return_value=(models, session)), patch(
        "utils.db.DBGroup"
    ) as db_group:
        db_group.return_value.get_or_create_user.return_value = user
        send_report_to_db({"new": True}, "user", "group", "report-id")

    assert existing_report.report == {"new": True}
    session.add.assert_not_called()
    session.commit.assert_called_once()
    session.close.assert_called_once()
