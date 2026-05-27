import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def load_env_vars(monkeypatch):
    monkeypatch.setenv("DB_CONN_STRING", "addfs")


@pytest.fixture
def client():
    return TestClient(app)