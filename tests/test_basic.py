from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_register_user():
    payload = {
        "nome": "Leo",
        "email": "leo@test.com",
        "idade": 25,
        "senha": "123456"
    }

    response = client.post("/api/v1/auth/register", json=payload)

    # Testa se criou corretamente
    assert response.status_code == 201
    data = response.json()
    assert "id" in data  # só podemos checar o 'id', que é o que o endpoint retorna

