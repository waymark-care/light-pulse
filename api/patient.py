from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from services import db_utils
from dependencies import get_current_active_user

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
