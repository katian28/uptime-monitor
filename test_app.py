import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_add_valid_url(client):
    res = client.post("/add", json={"url": "https://www.google.com"})
    assert res.status_code == 201
    assert "Monitoring started" in res.get_json()["message"]

def test_add_invalid_url(client):
    res = client.post("/add", json={})
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_status_response(client):
    client.post("/_reset")
    client.post("/add", json={"url": "https://www.google.com"})
    res = client.get("/status")
    assert res.status_code == 200
    data = res.get_json()
    assert "https://www.google.com" in data
    assert "status" in data["https://www.google.com"]
    assert "last_checked" in data["https://www.google.com"]
