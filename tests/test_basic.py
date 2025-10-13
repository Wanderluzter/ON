import mongomock
from fastapi.testclient import TestClient
from main import app

app.db = mongomock.MongoClient()["emotional_tracker"]

client = TestClient(app)

def test_register_user():
    response = client.post("/api/v1/auth/register", json={
        "nome": "Leo",
        "email": "leo@test.com",
        "idade": 25,
        "senha": "123456"
    })
    assert response.status_code == 201
    assert "id" in response.json()
