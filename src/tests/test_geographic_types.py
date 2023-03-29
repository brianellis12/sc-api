from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from app.authentication.routers import get_authenticated_user

from app.geographic_types.routers import router
from fastapi.testclient import TestClient
from database import db

# Create a new client for the test
@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_authenticated_user] = lambda: None
    yield TestClient(app)

# Test that the Get Geoid endpoint works as expected
def test_get_geoid(test_client):
    mock_latitude = "34.1668741"
    mock_longitude = "-112.4686757"
    mock_result = {
        "state": "04",
        "county": "025",
        "tract": "001402"
    }
    response = test_client.get("/geoid", params={"longitude": mock_longitude, "latitude": mock_latitude })

    assert response.status_code == 200

    assert response.json() == mock_result
