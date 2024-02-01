from datetime import timedelta
from typing import Annotated
import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from database import schemas
from database.db import engine, get_db
from services.db_utils import get_patient
from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    create_access_token,
    authenticate_user,
)
from dependencies import get_current_active_user

from api import patient

logger = logging.getLogger(__name__)


schemas.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(patient.router)

@app.get("/")
async def root():
    logger.info("Hello world")
    return {"message": "Hello world"}


# Health check endpoint
@app.get("/ping")
async def pong():
    return {"message": "pong"}


# API endpoint to get a patient by ID - testing that DB connection works
@app.get("/patients/{patient_id}")
async def read_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = get_patient(db, id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


# Authentication code
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# example route that requires authentication and getting the current user
@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[(schemas.Waymarker, Depends(get_current_active_user))],
    db: Session = Depends(get_db),
):
    return current_user
