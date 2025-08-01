from dotenv import load_dotenv
load_dotenv()
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from app.main import app
from app.database import Base, get_db


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


def test_login():
    Base.metadata.create_all(engine)
    client = TestClient(app)
    app.dependency_overrides[get_db] = get_db_override
    response = client.post('/token', data={
        'username': 'admin',
        'password': 'admin'
    })
    Base.metadata.drop_all(engine)
    assert response.status_code == 200, response.text