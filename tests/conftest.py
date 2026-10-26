import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app(":memory:"))


@pytest.fixture
def laptop(client: TestClient) -> dict:
    res = client.post("/items", json={"name": "노트북 A", "category": "노트북"})
    assert res.status_code == 201
    return res.json()
