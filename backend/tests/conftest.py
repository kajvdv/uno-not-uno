import pytest
from dotenv import load_dotenv
load_dotenv(".env.test")
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from backend.main import app


@pytest.fixture(name="app")
def app_fixture():
    return app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def runner():
    return CliRunner()