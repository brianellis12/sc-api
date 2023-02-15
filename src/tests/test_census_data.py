from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.census_data.routers import router
from fastapi.testclient import TestClient

# Create a new client for the tests
@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(router)
    yield TestClient(app)

# Test that the get sections endpoint works as expected
def test_get_group_sections(test_client):
    mock_group = "B29"
    mock_result = [
        {
            "section": "CITIZEN, VOTING-AGE POPULATION BY AGE"
        },
        {
            "section": "CITIZEN, VOTING-AGE POPULATION BY EDUCATIONAL ATTAINMENT"
        },
        {
            "section": "CITIZEN, VOTING-AGE POPULATION BY POVERTY STATUS"
        },
        {
            "section": "MEDIAN HOUSEHOLD INCOME FOR HOUSEHOLDS WITH A CITIZEN, VOTING-AGE HOUSEHOLDER (IN 2020 INFLATION-ADJUSTED DOLLARS)"
        }
    ]
    response = test_client.get("/location/sections", params={"group": mock_group})

    assert response.status_code == 200

    assert response.json() == mock_result

# Check that the get census data endpoint works as expected
def test_get_census_data(test_client):
    mock_state = "04" 
    mock_county = "025"
    mock_tract = "001402"
    mock_section = "MEDIAN AGE BY SEX"
    mock_result = [
        {
            "label": "Estimate!!Median age --!!Total:",
            "statistic": "62.6"
        },
        {
            "label": "Estimate!!Median age --!!Male",
            "statistic": "62.1"
        },
        {
            "label": "Estimate!!Median age --!!Female",
            "statistic": "64.5"
        }
    ]

    response = test_client.get("/location/data", params={"state": mock_state, "county": mock_county, "tract": mock_tract, "section": mock_section})

    assert response.status_code == 200

    assert response.json() == mock_result