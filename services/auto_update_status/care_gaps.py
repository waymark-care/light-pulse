from sqlalchemy.orm import Session
from ..db_utils import get_patient, update_patient_status
import logging

logger = logging.getLogger(__name__)


async def patient_care_gaps_update(db: Session, patient_id: str, total_gaps):
    patient = get_patient(db, patient_id)

    if not patient:
        return None, "Patient not found"
    if not patient.PatientList:
        return None, f"PatientList not found for patient {patient_id}"

    # sanity check to ensure data teams' data matches Lighthouse DB
    if patient.PatientList.qcgNumLikelyOpen != total_gaps:
        return (
            None,
            f"Total gaps {total_gaps} does not match database value"
            f" {patient.PatientList.qcgNumLikelyOpen}",
        )

    if patient.status == "ASSIGNED" and total_gaps > 0:
        updated_patient = update_patient_status(db, patient_id, "TARGETED")

        logger.info(f"Updated patient {patient_id} status to TARGETED")
        return updated_patient, None

    return None, None
