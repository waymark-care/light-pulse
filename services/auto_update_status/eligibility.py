from typing import List
from sqlalchemy.orm import Session
from services.db_utils import get_patient, update_patient_status
from models.patient import EligibilityStatus, PatientStatusTypes
import logging

logger = logging.getLogger(__name__)

target_status: List[PatientStatusTypes] = [
    "ASSIGNED",
    "TARGETED",
    "OUTREACH",
    "GRADUATED",
    "REFUSED_NO",
    "REFUSED_MAYBE",
    "DROPPED_OUT_OF_CONTACT",
    "WITHDRAWN_PATIENT",
    "WITHDRAWN_WAYMARK",
]


async def patient_eligibility_status(
    db: Session,
    patient_id: str,
    old_eligibility: EligibilityStatus,
    new_eligibility: EligibilityStatus,
):
    patient = get_patient(db, patient_id)
    if not patient:
        return None, "Patient not found"

    # sanity check to ensure data teams' data matches Lighthouse DB
    if patient.isEligible != new_eligibility:
        return (
            None,
            "Patient isEligible does not match newEligibility status",
        )

    if (
        old_eligibility == EligibilityStatus.ELIGIBLE
        and new_eligibility == EligibilityStatus.INELIGIBLE
        and patient.status in target_status
    ):
        updated_patient = update_patient_status(
            db, patient_id, PatientStatusTypes.NOT_ELIGIBLE
        )
        logger.info(f"Updated patient {patient_id} status to NOT_ELIGIBLE")

        return updated_patient, None

    if (
        old_eligibility == EligibilityStatus.INELIGIBLE
        and new_eligibility == EligibilityStatus.ELIGIBLE
    ):
        updated_patient = update_patient_status(
            db, patient_id, PatientStatusTypes.ASSIGNED
        )
        logger.info(f"Updated patient {patient_id} status to ASSIGNED")

        return updated_patient, None

    return None, None
