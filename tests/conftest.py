import pytest
from fastapi.testclient import TestClient
from src.main import app, get_db
import mongomock

# Cria um client de banco falso
@pytest.fixture
def test_db():
    client = mongomock.MongoClient()
    return client["emotional_tracker"]

# Substitui a dependência original do FastAPI pelo mock
@pytest.fixture(autouse=True)
def override_get_db(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)
