from fastapi.testclient import TestClient

from webapp.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/api/talk", params={"phrase": "Привет! Как дела?"})
    assert response.status_code == 200
    assert response.json()["response"] != ""
