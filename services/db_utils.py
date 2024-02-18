from sqlalchemy.orm import Session
from database.schemas import Patient, Waymarker, AdmissionDischargeTransfer
from models.waymarker import Waymarker as WaymarkerModel


def get_patient(db: Session, patient_id: str):
    return db.query(Patient).get(patient_id)


def update_patient_status(db: Session, id: str, status: str):
    patient = get_patient(db, id)
    patient.status = status
    db.commit()
    db.refresh(patient)
    return patient


def get_adt_event(db: Session, adt_event_id: str):
    return db.query(AdmissionDischargeTransfer).get(adt_event_id)


# ============ Waymarker methods ============
def get_waymarker(db: Session, waymarker_id: str):
    return db.query(Waymarker).get(waymarker_id)


def create_waymarker(
    db: Session,
    waymarker: WaymarkerModel,
):
    waymarker = Waymarker(
        id=waymarker.id,
        firstName=waymarker.firstName,
        lastName=waymarker.lastName,
        market=waymarker.market,
        email=waymarker.email,
        title=waymarker.title,
    )
    db.add(waymarker)
    db.commit()
    db.refresh(waymarker)
    return waymarker
