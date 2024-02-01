from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import get_db
from services.auto_update_status.care_gaps import patient_care_gaps_update
from services.auto_update_status.adt_events import adt_event_update
from dependencies import get_current_active_user

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    # requires authentication
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


class PatientCareGapRequestBody(BaseModel):
    patient_id: str
    total_gaps: int


@router.post("/care-gaps")
async def patient_care_gaps(
    care_gaps: PatientCareGapRequestBody,
    db: Session = Depends(get_db),
):
    """Updates patient status from
    ASSIGNED to TARGETED if there is more than one open care gap"""
    patient_id, total_gaps = care_gaps.patient_id, care_gaps.total_gaps
    result, error = await patient_care_gaps_update(db, patient_id, total_gaps)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result


class PatientAdtEventRequestBody(BaseModel):
    patient_id: str
    adtEventId: int


@router.post("/adt-event")
async def patient_adt_event(
    adt_event: PatientAdtEventRequestBody,
    db: Session = Depends(get_db),
):
    """Updates patient status from
    ASSIGNED to TARGETED with a relevant ADT event
    """
    patient_id, adt_event_id = adt_event.patient_id, adt_event.adtEventId
    result, error = await adt_event_update(db, patient_id, adt_event_id)

    if error:
        raise HTTPException(status_code=400, detail=error)
    return result
