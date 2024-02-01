from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Union

from passlib.context import CryptContext
from jose import jwt

from sqlalchemy.orm import Session
from models.waymarker import Waymarker
from services.db_utils import get_waymarker

SECRET_KEY = "3b99bb090543a635183501a25bb3436ade347e7de4b4b33ce584c5c2a8c3f39d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


def verify_password(plain_password, hashed_password):
    # return pwd_context.verify(plain_password, hashed_password)
    # TODO: remove this line when we are encrypting the password in the LH DB
    #       note that this reflects the current behavior in Shipyard
    return True


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    user = get_waymarker(db, id=username)
    if user:
        return Waymarker(**user.__dict__)


async def authenticate_user(db: Session, id: str, api_key: str):
    user = get_user(db, id)
    if not user:
        return False
    if not verify_password(api_key, get_password_hash(user.apiKey)):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
