import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, DeclarativeBase

DATABASE_URL = os.environ['DB_CONN_STRING']

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    ...

def get_db():
    with Session(engine) as db:
        yield db
