import os
from unittest.mock import Mock, patch
from types import SimpleNamespace
import pytest
from sqlalchemy import Column, Integer, String, create_engine
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
