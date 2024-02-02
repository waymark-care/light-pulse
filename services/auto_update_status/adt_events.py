from datetime import datetime
import logging

from sqlalchemy.orm import Session
from ..db_utils import get_patient, update_patient_status, get_adt_event
from models.patient import Patient, AdmissionDischargeTransfer

logger = logging.getLogger(__name__)


async def adt_event_update(db: Session, patient_id: str, adt_event_id: str):
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None, "Patient not found"

    patient = Patient(**db_patient.__dict__)

    db_adt_event = get_adt_event(db, adt_event_id)
    if not db_adt_event:
        return None, "No ADT Event Found"

    adt_event = AdmissionDischargeTransfer(**db_adt_event.__dict__)

    if adt_event.patientId != patient.id:
        return None, "ADT Event does not match patientId"

    event_date = get_adt_event_date(adt_event)

    if not event_date:
        return None, "No event date found"

    if not is_recent_event(event_date):
        return None, "Event date is not recent"

    # Update patient status to TARGETED if all conditions pass
    if patient.status == "ASSIGNED":
        updated_patient = update_patient_status(db, patient_id, "TARGETED")
        logger.info(f"Updated patient {patient_id} status to TARGETED")
        return updated_patient, None

    return None, None


def get_adt_event_date(adt_event: AdmissionDischargeTransfer):
    event_date = None
    if adt_event.dischargedDate:
        event_date = adt_event.dischargedDate
    else:
        event_date = adt_event.admittedDate

    return event_date


def is_recent_event(event_date: datetime):
    current_date = datetime.now()
    time_difference = current_date - event_date
    days_difference = time_difference.days

    return days_difference <= 7
