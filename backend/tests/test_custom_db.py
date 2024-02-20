import pytest
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base


@pytest.fixture
def mocked_db():
    # Create SQLAlchemy engine and session
    engine = create_engine("sqlite:///memory")
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()

    class EpRegistration(Base):
        __tablename__ = "ep_registration"
        id = Column(Integer, primary_key=True)
        otc_licence_id = Column(Integer, ForeignKey("otc_licence.id"))
        route_number = Column(String(255))
        route_description = Column(String(255))
        variation_number = Column(Integer)
        start_point = Column(String(255))
        finish_point = Column(String(255))
        via = Column(String(255))
        subsidised = Column(String(10))
        subsidy_detail = Column(String(255))
        is_short_notice = Column(Boolean)
        received_date = Column(Date)
        granted_date = Column(Date)
        effective_date = Column(Date)
        end_date = Column(Date)
        otc_operator_id = Column(Integer, ForeignKey("otc_operator.id"))
        bus_service_type_id = Column(String(255))
        bus_service_type_description = Column(String(255))
        registration_number = Column(String(255))
        traffic_area_id = Column(String(255))
        application_type = Column(String(255))
        publication_text = Column(String(255))
        other_details = Column(String(255))

    class OtcLicence(Base):
        __tablename__ = "otc_licence"
        id = Column(Integer, primary_key=True)
        licence_number = Column(String(255), unique=True)
        licence_status = Column(String(255))
        otc_licence_id = Column(Integer, unique=True)

    class OtcOperator(Base):
        __tablename__ = "otc_operator"
        id = Column(Integer, primary_key=True)
        operator_name = Column(String(255))
        operator_id = Column(Integer, unique=True)

    Base.metadata.create_all(engine)

    yield session

    # Clean up after the test
    session.close()
    engine.dispose()


# use the fixture in the test
def test_add_record(mocked_db):
    # Add a record to the database
    record = MockData().get_mock_data()
    mocked_db.add(record)
    mocked_db.commit()

    # Get the record from the database
    result = mocked_db.query(EpRegistration).first()

    # Assert that the record is the same as the one added
    assert result == record
