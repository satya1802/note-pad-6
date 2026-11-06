"""Integration tests for account registration, sign-in, sign-out and session identity."""

import uuid

from app import create_app

MIN_PASSWORD = "correct-horse"


def _client():
    app = create_app()
    app.testing = True
    return app.test_client()


def _email() -> str:
    return f"user-{uuid.uuid4()}@example.com"


def test_ac001_register_creates_account_and_active_session() -> None:
    client = _client()
    email = _email()

    response = client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})

    assert response.status_code == 201
    body = response.get_json()
    assert body["user"]["email"] == email
    assert "password" not in body["user"]
    assert "password_hash" not in body["user"]

    # The session started by registration is active: /me succeeds without a fresh login.
    me = client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.get_json()["user"]["email"] == email


def test_ac002_register_duplicate_email_returns_409() -> None:
    client = _client()
    email = _email()
    client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})

    response = client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})

    assert response.status_code == 409
    assert "already" in response.get_json()["message"].lower()


def test_ac003_register_invalid_email_and_short_password_returns_422() -> None:
    client = _client()

    response = client.post(
        "/api/auth/register", json={"email": "not-an-email", "password": "short"}
    )

    assert response.status_code == 422
    fields = response.get_json()["fields"]
    assert "email" in fields
    assert "password" in fields


def test_ac004_login_with_correct_credentials_starts_session() -> None:
    client = _client()
    email = _email()
    client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})
    client.post("/api/auth/logout")

    response = client.post("/api/auth/login", json={"email": email, "password": MIN_PASSWORD})

    assert response.status_code == 200
    assert response.get_json()["user"]["email"] == email

    me = client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.get_json()["user"]["email"] == email


def test_ac005_login_wrong_credentials_returns_single_generic_401() -> None:
    client = _client()
    email = _email()
    client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})
    client.post("/api/auth/logout")

    wrong_password = client.post("/api/auth/login", json={"email": email, "password": "nope12345"})
    wrong_email = client.post(
        "/api/auth/login", json={"email": _email(), "password": MIN_PASSWORD}
    )

    assert wrong_password.status_code == 401
    assert wrong_email.status_code == 401
    # Identical body for both failure modes: nothing distinguishes which field was wrong.
    assert wrong_password.get_json() == wrong_email.get_json()


def test_ac006_logout_ends_session() -> None:
    client = _client()
    email = _email()
    client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})

    response = client.post("/api/auth/logout")
    assert response.status_code == 200

    me = client.get("/api/auth/me")
    assert me.status_code == 401


def test_ac007_me_returns_401_without_active_session() -> None:
    client = _client()

    response = client.get("/api/auth/me")

    assert response.status_code == 401
