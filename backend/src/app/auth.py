from subprocess import Popen
import logging
import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Form, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError
from sqlalchemy import String, Integer, Column, insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import Base, get_db


ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
REFRESH_TOKEN_SECRET = os.environ["REFRESH_TOKEN_SECRET"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

logger = logging.getLogger(__name__)
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

class User(Base):
    __tablename__ = "user"

    username = Column(String, primary_key=True)
    password = Column(String)

    def __repr__(self) -> str:
        return f"username={self.username} password={self.password}"


def decode_token(token):
    return jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])


def get_current_user(token = Depends(oath2_scheme)):
    user = decode_token(token)['sub']
    return user


def generate_access_token(name, days=0, minutes=15):
    access_token = jwt.encode(
        {"sub": name, 'exp': datetime.now(timezone.utc) + timedelta(days=days, minutes=minutes)},
        key=os.environ["ACCESS_TOKEN_SECRET"],
        algorithm="HS256"
    )
    return access_token

def generate_refresh_token(name, days=0, minutes=0):
    refresh_token = jwt.encode(
        {"sub": name, 'exp': datetime.now(timezone.utc) + timedelta(days=days, minutes=minutes)},
        key=os.environ["REFRESH_TOKEN_SECRET"],
        algorithm="HS256"
    )
    return refresh_token


invalid_response = HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
@router.post('/token')
def get_token(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    stmt = select(User).where(User.username == form.username)
    row = db.execute(stmt).first()
    if not row:
        raise invalid_response
    print(row.User)
    hashed_password = row.User.password
    if not pwd_context.verify(form.password, hashed_password):
        raise invalid_response
    access_token = generate_access_token(form.username, minutes=15)
    refresh_token = generate_refresh_token(form.username, days=0, minutes=15)
    response.set_cookie('refresh_token', refresh_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh_token(request: Request):
    refresh_token = request.cookies['refresh_token']
    sub, _ = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM]).values()
    new_access_token = jwt.encode(
        {"sub": sub, 'exp': datetime.now(timezone.utc) + timedelta(minutes=15)},
        key=ACCESS_TOKEN_SECRET,
        algorithm=ALGORITHM
    )
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post('/register', status_code=204)
def register_user(username = Form(), password = Form(), db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, password=hashed_password)
    db.add(user)
    try:
        db.commit()
    except IntegrityError as e:
        logger.error("User already exists")
        db.rollback()
        raise HTTPException(status_code=400, detail='User already exists')


@router.get('/users/me')
def get_user(user = Depends(get_current_user)):
    return user
