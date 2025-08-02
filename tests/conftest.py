from dotenv import load_dotenv
load_dotenv()
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session

from app.database import Base, get_db
from app.main import app
from app.testclient import Client


engine = create_engine(
    "sqlite://",
    connect_args={
        'check_same_thread': False
    },
    poolclass=StaticPool
)

def get_db_override():
    with Session(engine) as db:
        yield db

app.dependency_overrides[get_db] = get_db_override

@pytest.fixture
def db():
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(db):
    testclient = TestClient(app)
    # testclient = AsyncClient(app)
    client = Client(testclient)
    with testclient:
        yield client
    # client.reset_lobbies()
