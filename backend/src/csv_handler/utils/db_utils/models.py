from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class OTCLicence(declarative_base):
    __tablename__ = "otc_licence"

    id = Column(Integer, primary_key=True)
    licence_number = Column(String(255), unique=True)
    licence_status = Column(String(255))

    def __repr__(self):
        return f"OTCLicence(id={self.id}, licence_number={self.licence_number}, licence_status={self.licence_status})"


class PDBRDRegistration(Base):
    __tablename__ = "pdbrd_registration"

    id = Column(Integer, primary_key=True)
    otc_licence_id = Column(Integer)
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
    operator = relationship("OTCOperator", back_populates="pdbrd_registration")

    def __repr__(self):
        return f"PDBRDRegistration(id={self.id}, route_number={self.route_number}, route_description={self.route_description}, variation_number={self.variation_number}, start_point={self.start_point}, finish_point={self.finish_point}, via={self.via}, subsidised={self.subsidised}, subsidy_detail={self.subsidy_detail}, is_short_notice={self.is_short_notice}, received_date={self.received_date}, granted_date={self.granted_date}, effective_date={self.effective_date}, end_date={self.end_date}, otc_operator_id={self.otc_operator_id}, bus_service_type_id={self.bus_service_type_id}, bus_service_type_description={self.bus_service_type_description}, registration_number={self.registration_number}, traffic_area_id={self.traffic_area_id}, application_type={self.application_type}, publication_text={self.publication_text}, other_details={self.other_details})"


class OTCOperator(Base):
    __tablename__ = "otc_operator"

    id = Column(Integer, primary_key=True)
    operator_name = Column(String(255))

    def __repr__(self):
        return f"OTCOperator(id={self.id}, operator_name={self.operator_name})"
