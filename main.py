from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session

from src import crud, models
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello world"}


# Health check endpoint
@app.get("/ping")
async def pong():
    return {"message": "pong"}


# API endpoint to get a patient by ID - testing that DB connection works
@app.get("/patients/{patient_id}")
async def read_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient
