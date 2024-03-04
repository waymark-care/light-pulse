from sqlalchemy.orm import Session
from database.schemas import (
    Patient,
    Waymarker,
    AdmissionDischargeTransfer,
    TwilioNumber,
)
from models.waymarker import Waymarker as WaymarkerModel
from cuid import cuid


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
    try: 
        waymarker = Waymarker(
            id=waymarker.id,
            firstName=waymarker.firstName,
            lastName=waymarker.lastName,
            market=waymarker.market,
            email=waymarker.email,
            title=waymarker.title,
            phoneNumber=waymarker.phoneNumber,
        )
        db.add(waymarker)
        db.commit()
    except Exception as e: 
        db.rollback()
        raise Exception(f"Database error: {e}")
    
    db.refresh(waymarker)
    return waymarker


def add_twilio_phone_number(
    db: Session,
    waymarker_id: str,
    twilio_number: str,
):
    phone_number_link = TwilioNumber(
        id=cuid(), number=twilio_number, waymarkerId=waymarker_id
    )
    db.add(phone_number_link)
    db.commit()
    return phone_number_link
