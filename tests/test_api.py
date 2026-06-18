from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_plan_endpoint():
    response = client.get("/plan", params={"destination": "Madrid", "days": 4})
    assert response.status_code == 200
    assert response.json()["destination"] == "Madrid"
