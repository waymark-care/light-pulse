from sqlalchemy.orm import Session
from database.schemas import Patient, Waymarker


def get_patient(db: Session, id: str):
    return db.query(Patient).filter(Patient.id == id).first()


def get_waymarker(db: Session, id: str):
    return db.query(Waymarker).filter(Waymarker.id == id).first()


def update_patient_status(db: Session, id: str, status: str):
    patient = get_patient(db, id)
    patient.status = status
    db.commit()
    db.refresh(patient)
    return patient
