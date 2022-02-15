import pytest
from fastapi.testclient import TestClient

from webapp.main import app


client = TestClient(app)


@pytest.mark.run(order=1)
def test_read_main():
    response = client.get("/api/v1/talk", params={"phrase": "Привет! Как дела?"})
    assert response.status_code == 200
    assert response.json()["response"] != ""


@pytest.mark.run(order=5)
def test_history():
    response = client.get("/api/v1/talk/history")
    assert response.status_code == 200
    assert response.json()["history"] != ""


if __name__ == "__main__":
    pytest.main()
