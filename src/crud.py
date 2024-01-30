from sqlalchemy.orm import Session

from . import models


def get_patient(db: Session, id: str):
    return db.query(models.Patient).filter(models.Patient.id == id).first()


def get_waymarker(db: Session, id: str):
    return db.query(models.Waymarker).filter(models.Waymarker.id == id).first()
