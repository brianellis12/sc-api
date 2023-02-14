from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.census_data.routers import router
from database import db, integration, crud

@pytest.fixture
def fake():
    return Faker()

@pytest.fixture
def test_client():
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[db.get_db] = db.create_session()
    yield TestClient(app)

def test_get_group_sections(test_client):
    mock_group = "TRANSPORTATION"

    response = test_client.get("/location/sections", params={"group": mock_group})

    assert response.status_code == 200