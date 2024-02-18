import logging

from sqlalchemy.orm import Session
from ..db_utils import get_patient, update_patient_status
from models.patient import RiskTier

logger = logging.getLogger(__name__)


async def patient_risk_tier_update(
    db: Session,
    patient_id: str,
    risk_tier: RiskTier,
):
    patient = get_patient(db, patient_id)
    if not patient:
        return None, "Patient not found"

    if not patient.PatientList:
        return None, f"PatientList not found for patient {patient_id}"

    logger.info(f"Risk Tier: {risk_tier} for patient {RiskTier.HIGH}")

    if risk_tier == RiskTier.HIGH and patient.status == "ASSIGNED":
        updated_patient = update_patient_status(db, patient_id, "TARGETED")
        logger.info(f"Updated patient {patient_id} status to TARGETED")
        return updated_patient, None
    return None, None
