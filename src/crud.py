from sqlalchemy.orm import Session

from . import models


def get_patient(db: Session, id: str):
    return db.query(models.Patient).filter(models.Patient.id == id).first()


def get_waymarker(db: Session, id: str):
    return db.query(models.Waymarker).filter(models.Waymarker.id == id).first()


def update_patient_status(db: Session, id: str, status: str):
    patient = get_patient(db, id)
    patient.status = status
    db.commit()
    db.refresh(patient)
    return patient
