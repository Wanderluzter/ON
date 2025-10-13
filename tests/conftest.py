# tests/conftest.py
import pytest
import mongomock
from src.main import app, get_db
from fastapi.testclient import TestClient

@pytest.fixture(scope="function")
def mock_db():
    client = mongomock.MongoClient()
    db = client["emotional_tracker"]
    yield db

@pytest.fixture(scope="function")
def client(mock_db):
    # Sobrescreve o get_db para retornar o mock
    app.dependency_overrides[get_db] = lambda: mock_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
