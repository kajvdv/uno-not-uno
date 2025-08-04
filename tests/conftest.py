import os
import pytest
# import pytest_asyncio
from fastapi.testclient import TestClient
# from httpx import AsyncClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from httpx import ASGITransport

from app.client import Client


# Modules are imported inside the fixture to ensure env vars are loaded before importing
@pytest.fixture(autouse=True)
def load_envvars(tmpdir):
    from dotenv import load_dotenv
    load_dotenv()
    os.environ['LOBBIES_DIR'] = str(tmpdir / 'lobbies')


@pytest.fixture
def db():
    from app.database import Base
    import app.main # Make sure that all the models added to Base
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db


@pytest.fixture(name='app_setup')
async def app_setup_fixture(db):
    from app.main import app
    from app.database import get_db
    def get_session_override():  
        return db
    app.dependency_overrides[get_db] = get_session_override
    app.debug = True
    return app


@pytest.fixture(name='app')
async def app_fixture(app_setup):
    from asgi_lifespan import LifespanManager
    async with LifespanManager(app_setup) as manager:
        yield manager.app


@pytest.fixture(name='client')
async def client_fixture(app):
    print("Getting client")
    return Client(transport=ASGITransport(app=app), base_url="http://testserver")


@pytest.fixture(params=['admin', 'testuser'])
def username(request, client):
    password = 'password'
    print("Regisering user")
    with client:
        client.register(request.param, password)
        client.login(request.param, password)
        return request.param

@pytest.fixture(name='user', params=['admin', 'testuser'])
async def user_fixture(request, client):
    password = 'password'
    await client.register(request.param, password)
    await client.login(request.param, password)
    return request.param


@pytest.fixture
def with_lobbies(client: Client, lobbies):
    with client:
        for lobby in lobbies:
            name, size, ai_count = lobby
            client.create_lobby(
                name=name,
                size=size,
                aiCount=ai_count
            )
