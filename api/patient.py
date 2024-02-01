from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import get_db
from services.auto_update_status.care_gaps import patient_care_gaps_update
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
    patient_id, total_gaps = care_gaps.patient_id, care_gaps.total_gaps
    result, error = await patient_care_gaps_update(db, patient_id, total_gaps)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result
