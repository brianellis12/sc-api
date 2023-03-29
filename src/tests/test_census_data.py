from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from app.authentication.routers import get_authenticated_user

from app.census_data.routers import router
from fastapi.testclient import TestClient

"""
Create a new client for the tests
"""
@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_authenticated_user] = lambda: None
    yield TestClient(app)

"""
Test that the get sections endpoint works as expected
"""
def test_get_group_sections(test_client):
    mock_group = "B04"
    mock_result = [
    "PEOPLE REPORTING MULTIPLE ANCESTRY",
    "PEOPLE REPORTING SINGLE ANCESTRY",
    "ANCESTRY",
    "PEOPLE REPORTING ANCESTRY"
]
    response = test_client.get("/location/sections", params={"group": mock_group})

    assert response.status_code == 200

    assert response.json() == mock_result

"""
Check that the get census data endpoint works as expected
"""
def test_get_census_data(test_client):
    mock_state = "04" 
    mock_county = "025"
    mock_tract = "001402"
    mock_section = "MEDIAN AGE BY SEX"
    mock_result = [
    " Median age --Total: 62.6",
    " Median age -- Male: 62.1",
    " Median age -- Female: 64.5"
]

    response = test_client.get("/location/data", params={"state": mock_state, "county": mock_county, "tract": mock_tract, "section": mock_section})

    assert response.status_code == 200

    assert response.json() == mock_result