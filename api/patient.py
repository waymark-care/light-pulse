from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import get_db
from services.auto_update_status.care_gaps import patient_care_gaps_update
from services.auto_update_status.adt_events import adt_event_update
from services.auto_update_status.eligibility import patient_eligibility_status

from services import db_utils
from dependencies import get_current_active_user

from models.patient import EligibilityStatus

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    # requires authentication
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


# API endpoint to get a patient by ID - testing that DB connection works
@router.get("/{patient_id}")
async def read_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = db_utils.get_patient(db=db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


class PatientCareGapRequestBody(BaseModel):
    total_gaps: int


@router.post("/{patient_id}/care-gaps")
async def patient_care_gaps(
    patient_id: str,
    care_gaps: PatientCareGapRequestBody,
    db: Session = Depends(get_db),
):
    """Updates patient status from
    ASSIGNED to TARGETED if there is more than one open care gap"""
    total_gaps = care_gaps.total_gaps
    result, error = await patient_care_gaps_update(db, patient_id, total_gaps)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result


class PatientAdtEventRequestBody(BaseModel):
    adtEventId: str


@router.post("/{patient_id}/adt-event")
async def patient_adt_event(
    patient_id: str,
    adt_event: PatientAdtEventRequestBody,
    db: Session = Depends(get_db),
):
    """Updates patient status from
    ASSIGNED to TARGETED with a relevant ADT event
    """
    adt_event_id = adt_event.adtEventId
    result, error = await adt_event_update(db, patient_id, adt_event_id)

    if error:
        raise HTTPException(status_code=400, detail=error)
    return result


class PatientEligibilityRequestBody(BaseModel):
    old_eligibility: EligibilityStatus
    new_eligibility: EligibilityStatus


@router.post("/{patient_id}/eligibility-status")
async def update_patient_eligibility_status(
    patient_id: str,
    eligibility: PatientEligibilityRequestBody,
    db: Session = Depends(get_db),
):
    """Run through an eligibility calculator for a given patient
    and auto-assign the patient.status"""
    old_eligibility, new_eligibility = (
        eligibility.old_eligibility,
        eligibility.new_eligibility,
    )
    result, error = await patient_eligibility_status(
        db, patient_id, old_eligibility, new_eligibility
    )

    if error:
        raise HTTPException(status_code=400, detail=error)
    return result
