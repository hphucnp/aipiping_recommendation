from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_request_recommendations():
    response = client.post("/recommendations?country=USA&season=summer")
    assert response.status_code == 200
    assert "country" in response.json()
    assert "season" in response.json()
    assert "recommendations" in response.json()
    assert "status" in response.json()


def test_get_recommendation():
    # You'll need to replace 'test_uid' with a valid uid from your database
    response = client.get("/recommendations/test_uid")
    assert response.status_code == 200
    assert "country" in response.json()
    assert "season" in response.json()
    assert "recommendations" in response.json()
    assert "status" in response.json()
