import json
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models.auth import AuthSession, AuthUser
from app.services.auth_service import initialize_auth, password_hasher, token_digest

pytestmark = pytest.mark.auth
PASSWORD = "test-only-password"


@pytest.fixture
def auth_client(monkeypatch):
    engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    accounts = [
        {"email": "admin@example.test", "display_name": "Administrador", "role": "admin", "password_hash": password_hasher.hash(PASSWORD)},
        {"email": "user@example.test", "display_name": "Usuario", "role": "user", "password_hash": password_hasher.hash(PASSWORD)},
    ]
    monkeypatch.setattr(settings, "pilot_accounts_json", SecretStr(json.dumps(accounts)))
    initialize_auth(engine)

    def db_override():
        with Session(engine) as db:
            yield db

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = db_override
    yield TestClient(app), engine
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)
    engine.dispose()


def sign_in(client, email="user@example.test"):
    result = client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
    assert result.status_code == 200
    assert result.headers["cache-control"] == "no-store"
    body = result.json()
    return body, {"Authorization": f"Bearer {body['access_token']}"}


def test_login_normalizes_email_and_never_returns_password(auth_client):
    client, engine = auth_client
    body, headers = sign_in(client, " ADMIN@EXAMPLE.TEST ")
    assert body["user"]["role"] == "admin"
    assert PASSWORD not in json.dumps(body)
    assert "password_hash" not in json.dumps(body)
    assert datetime.fromisoformat(body["expires_at"]) > datetime.now(UTC)
    assert client.get("/api/v1/auth/me", headers=headers).json() == body["user"]
    assert client.get("/api/v1/students", headers=headers).status_code == 200
    with Session(engine) as db:
        stored = db.get(AuthSession, token_digest(body["access_token"]))
        assert stored is not None
        assert stored.token_hash != body["access_token"]


@pytest.mark.parametrize("method,path", [
    ("get", "/api/v1/students"), ("get", "/api/v1/cases"),
    ("get", "/api/v1/curriculum/concepts"), ("get", "/api/v1/ai-health/competencies"),
    ("post", "/api/v1/sessions/start"), ("post", "/api/v1/sessions/attempts/core"),
    ("post", "/api/v1/reasoning/analyze"), ("post", "/api/v1/tutor/turn"),
    ("post", "/api/v1/simulation/simulate"), ("post", "/api/v1/ai-health/evaluate"),
])
def test_educational_endpoints_require_auth(auth_client, method, path):
    client, _ = auth_client
    assert getattr(client, method)(path).status_code == 401


def test_roles_and_revocation(auth_client):
    client, _ = auth_client
    _, user_headers = sign_in(client)
    assert client.get("/api/v1/auth/users", headers=user_headers).status_code == 403
    _, admin_headers = sign_in(client, "admin@example.test")
    users = client.get("/api/v1/auth/users", headers=admin_headers)
    assert users.status_code == 200
    assert len(users.json()) == 2
    assert "password" not in users.text
    assert client.post("/api/v1/auth/logout", headers=user_headers).status_code == 204
    assert client.get("/api/v1/auth/me", headers=user_headers).status_code == 401
    assert client.get("/api/v1/auth/me", headers=admin_headers).status_code == 200


def test_expired_or_disabled_sessions_are_rejected(auth_client):
    client, engine = auth_client
    body, headers = sign_in(client)
    with Session(engine) as db:
        db.get(AuthSession, token_digest(body["access_token"])).expires_at = datetime.now(UTC) - timedelta(seconds=1)
        db.commit()
    assert client.get("/api/v1/students", headers=headers).status_code == 401
    body, headers = sign_in(client)
    with Session(engine) as db:
        db.get(AuthUser, body["user"]["id"]).active = False
        db.commit()
    assert client.get("/api/v1/students", headers=headers).status_code == 401


def test_login_lockout_recovers_after_timeout(auth_client):
    client, engine = auth_client
    for _ in range(5):
        response = client.post("/api/v1/auth/login", json={"email": "user@example.test", "password": "wrong"})
        assert response.status_code == 401
    assert client.post("/api/v1/auth/login", json={"email": "user@example.test", "password": PASSWORD}).status_code == 401
    with Session(engine) as db:
        user = db.scalar(select(AuthUser).where(AuthUser.email == "user@example.test"))
        user.locked_until = datetime.now(UTC) - timedelta(seconds=1)
        db.commit()
    sign_in(client)


def test_unknown_user_and_validation_do_not_expose_credentials(auth_client):
    client, _ = auth_client
    assert client.post("/api/v1/auth/login", json={"email": "unknown@example.test", "password": PASSWORD}).status_code == 401
    response = client.post("/api/v1/auth/login", json={"email": "user@example.test", "password": "sensitive" * 100})
    assert response.status_code == 422
    assert "sensitive" not in response.text
    assert client.get("/health").status_code == 200


def test_bootstrap_preserves_existing_account_changes(auth_client):
    _, engine = auth_client
    with Session(engine) as db:
        user = db.scalar(select(AuthUser).where(AuthUser.email == "user@example.test"))
        user.active = False
        db.commit()
    initialize_auth(engine)
    with Session(engine) as db:
        assert len(list(db.scalars(select(AuthUser)))) == 2
        assert db.scalar(select(AuthUser).where(AuthUser.email == "user@example.test")).active is False
