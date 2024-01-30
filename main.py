from datetime import timedelta
from typing import Annotated
import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

from auth import (
    Token,
    TokenData,
    SECRET_KEY,
    ALGORITHM,
    get_user,
    authenticate_user,
    create_access_token,
)

logger = logging.getLogger(__name__)


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
    logger.info("Hello world")
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


# Authentication code
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db=Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.Waymarker, Depends(get_current_user)]
) -> schemas.Waymarker:
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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


@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[schemas.Waymarker, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return current_user
