from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Support Ticket API is Working"
    }


def test_create_ticket():
    ticket = {
        "customer_name": "Test User",
        "title": "Login problem",
        "description": "Unable to login to my account.",
        "priority": "high"
    }

    response = client.post("/tickets/", json=ticket)

    assert response.status_code == 200
    assert response.json()["title"] == "Login problem"

def test_invalid_priority():
    ticket = {
        "customer_name": "Test User",
        "title": "Login problem",
        "description": "Unable to login to my account.",
        "priority": "urgent"
    }

    response = client.post("/tickets/", json=ticket)

    assert response.status_code == 422