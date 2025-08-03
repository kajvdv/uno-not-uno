import os
import pytest
from fastapi.testclient import TestClient
# from httpx import AsyncClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session


# Modules are imported inside the fixture to ensure env vars are loaded before importing
@pytest.fixture(autouse=True)
def load_envvars(tmpdir):
    from dotenv import load_dotenv
    load_dotenv()
    os.environ['LOBBIES_DIR'] = str(tmpdir)


@pytest.fixture()
def db():
    from app.database import Base
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db


@pytest.fixture
def client(db):
    from app.main import app
    from app.testclient import Client
    from app.database import get_db

    def get_session_override():  
        return db
    app.dependency_overrides[get_db] = get_session_override
    return Client(TestClient(app))


@pytest.fixture(params=['admin', 'testuser'], autouse=True)
def username(request, client, db):
    password = 'password'
    print("Regisering user")
    with client:
        client.register(request.param, password)
        client.login(request.param, password)
        return request.param

