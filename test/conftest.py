from app.main import app
from pytest import fixture
from fastapi.testclient import TestClient


@fixture(scope="module")
def test_client():
    return TestClient(app)
