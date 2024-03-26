import os
from unittest.mock import Mock, patch
import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

from utils.db import AutoMappingModels, DBManager, add_or_get_record, CreateEngine

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
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class TestCreateEngine:
    @patch("utils.db.print", return_value="test")
    @patch("utils.db.get_secret", return_value="test")
    @patch("utils.db.exit", return_value="test")
    @patch("utils.db.PROJECT_ENV", return_value="test")
    @patch("utils.pydant_model.getenv", return_value="test")
    def test_get_db_creds(
        cls, mock_getenv, mock_dbcreds, mock_exit, mock_secret, mock_print
    ):
        create_engine = CreateEngine.get_db_creds()
        with pytest.raises(Exception):
            create_engine.get_db_creds()
        # mock_dbcreds.assert_called()
        mock_exit.assert_called()
        mock_exit.assert_called_with(1)
        mock_secret.assert_called()
        mock_print.assert_called_with(
            "The error 'string indices must be integers, not 'str'' occurred"
        )


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
        return AutoMappingModels()

    def test_get_tables(self, auto_mapping_models):
        tables = auto_mapping_models.get_tables()
        assert isinstance(tables, dict)
        assert "EPRegistration" in tables
        assert "OTCOperator" in tables
        assert "OTCLicence" in tables
        assert isinstance(
            tables["EPRegistration"], type(auto_mapping_models.EPRegistration)
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
