import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from backend.main import app


@pytest.fixture(autouse=True)
def load_env_vars(monkeypatch):
    monkeypatch.setenv("DB_CONN_STRING", "addfs")


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