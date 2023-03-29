from copy import deepcopy
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.authentication.routers import get_authenticated_user
from app.user import routers as user_routers
from database import crud, db


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(user_routers.public)
    app.include_router(user_routers.authenticated)
    app.dependency_overrides[db.get_db] = lambda: None
    app.dependency_overrides[get_authenticated_user] = lambda: None

    yield TestClient(app)


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def fake_request_users(fake):
    request_users = []
    for _ in range(5):
        request_users.append(
            {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
            }
        )

    return request_users


@pytest.fixture
def fake_response_users(fake, fake_request_users):
    response_users = []

    for i in range(len(fake_request_users)):
        response_user = deepcopy(fake_request_users[i])
        response_user.update(
            {
                "id": fake.pyint(),
            }
        )
        response_users.append(response_user)

    return response_users


def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_add_user(test_app, fake_request_users, fake_response_users, monkeypatch):
    request_payload = fake_request_users[0]
    response_payload = fake_response_users[0]
    
    def mock_create_user(*args, **kwargs):
        return response_payload

    monkeypatch.setattr(crud.user, "create", staticmethod(mock_create_user))

    response = test_app.post("/users", json=request_payload)
    assert response.status_code == 200
    assert response.json() == response_payload


def test_get_users(test_app, fake_response_users, monkeypatch):
    def mock_get_all_users(*args, **kwargs):
        return fake_response_users

    monkeypatch.setattr(crud.user, "get_all", staticmethod(mock_get_all_users))

    response = test_app.get("/users")
    assert response.status_code == 200
    assert response.json() == fake_response_users


def test_get_user(test_app, fake_response_users, monkeypatch):
    response_payload = fake_response_users[1]

    def mock_get_user(*args, **kwargs):
        return response_payload

    monkeypatch.setattr(crud.user, "get", staticmethod(mock_get_user))

    response = test_app.get("/users/1")
    assert response.status_code == 200
    assert response.json() == response_payload


def test_update_user(test_app, fake_request_users, fake_response_users, monkeypatch):
    request_payload = fake_request_users[2]
    response_payload = fake_response_users[2]

    def mock_update_user(*args, **kwargs):
        return response_payload

    monkeypatch.setattr(crud.user, "update", staticmethod(mock_update_user))

    response = test_app.put("/users/3", json=request_payload)
    assert response.status_code == 200
    assert response.json() == response_payload


