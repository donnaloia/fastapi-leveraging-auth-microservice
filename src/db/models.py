from sqlalchemy import (
    Column, 
    Integer, 
    UUID,
    String, 
    Boolean, 
    TIMESTAMP, 
    text,
    ForeignKey
)
import uuid

from src.db.database import Base
from sqlalchemy.orm import relationship



class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))


class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"))
    organization = relationship("Organization")


class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    application_id = Column(UUID(as_uuid=True), ForeignKey("application.id"))
    application = relationship("Application")