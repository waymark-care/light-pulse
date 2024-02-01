from sqlalchemy import Table
from sqlalchemy.orm import relationship

from .db import lighthouse_metadata, engine, Base


class Patient(Base):
    __table__ = Table("Patient", lighthouse_metadata, autoload=engine)
    PatientList = relationship("PatientList", uselist=False)


class PatientList(Base):
    __table__ = Table("PatientList", lighthouse_metadata, autoload=engine)


class Waymarker(Base):
    __table__ = Table("Waymarker", lighthouse_metadata, autoload=engine)
