from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import jwt
import pytest

from app.auth import routers as auth_routers
from app.config import Settings, get_settings
from database import auth, db


def get_fake_settings():
    return Settings(
        token_key="fakeKey",
        db_connection_string="fakeDbConnection",
        oauth_android_client_id="fakeAndroidClient",
        oauth_desktop_client_id="fakeDesktopClient",
        oauth_ios_client_id="fakeIosClientId",
        oauth_web_client_id="fakeWebClientId",
        environment="fakeEnvironment",
    )


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(auth_routers.router)
    app.dependency_overrides[get_settings] = get_fake_settings
    app.dependency_overrides[db.get_db] = lambda: None
    yield TestClient(app)


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def fake_auth_request(fake):
    return {
        "token": fake.word(),
    }


@pytest.fixture
def fake_auth_response(fake):
    user = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "id": fake.pyint(),
    }
    return {"access_token": fake.word(), "user": user, "new_user": fake.pybool()}


def test_authenticate(test_app, fake_auth_request, fake_auth_response, monkeypatch):
    def mock_authenticate(*args, **kwargs):
        return fake_auth_response

    monkeypatch.setattr(auth.auth, "authenticate", mock_authenticate)

    response = test_app.post("/auth/authenticate", json=fake_auth_request)
    assert response.status_code == 200
    assert response.json() == fake_auth_response


def test_create_access_token(fake):
    user_id = fake.pyint()
    access_token_data: dict = {
        "sub": user_id,
        "user_id": user_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }
    settings = get_fake_settings()
    encoded_jwt = jwt.encode(access_token_data, settings.token_key)

    token = auth.auth.create_access_token(access_token_data, settings)
    assert token == encoded_jwt
