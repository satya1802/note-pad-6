"""Integration tests for the bearer-token session mechanism itself.

Every other integration test in this suite reuses one `app.test_client()` across a
whole scenario, so it rides on the Flask-Login session *cookie* `login_user()` sets --
exactly the mechanism the architecture says the deployed frontend cannot rely on,
because the API and the SPA sit on different origins. What actually has to work once
deployed is the `token` register/login hand back in the JSON body, sent on every later
call as `Authorization: Bearer <token>` with no cookie at all. Nothing else in this
repository exercises that path end to end, so these tests create one client to obtain
the token and then authenticate an entirely separate, cookie-free client with it.
"""

import uuid

from app import create_app

MIN_PASSWORD = "correct-horse"


def _client():
    app = create_app()
    app.testing = True
    return app.test_client()


def _email() -> str:
    return f"user-{uuid.uuid4()}@example.com"


def _bearer_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_register_response_carries_a_usable_bearer_token() -> None:
    issuing_client = _client()
    email = _email()

    register = issuing_client.post(
        "/api/auth/register", json={"email": email, "password": MIN_PASSWORD}
    )
    assert register.status_code == 201
    token = register.get_json().get("token")
    assert isinstance(token, str)
    assert len(token) > 10

    # A brand-new client that never saw the registration response, and so holds none
    # of its Set-Cookie: only the Authorization header can be authenticating it.
    bearer_client = _client()
    me = bearer_client.get("/api/auth/me", headers=_bearer_headers(token))

    assert me.status_code == 200
    assert me.get_json()["user"]["email"] == email


def test_login_response_carries_a_usable_bearer_token_after_the_original_session_ends() -> None:
    issuing_client = _client()
    email = _email()
    issuing_client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})
    issuing_client.post("/api/auth/logout")

    login = issuing_client.post("/api/auth/login", json={"email": email, "password": MIN_PASSWORD})
    assert login.status_code == 200
    token = login.get_json().get("token")
    assert isinstance(token, str)

    bearer_client = _client()
    me = bearer_client.get("/api/auth/me", headers=_bearer_headers(token))

    assert me.status_code == 200
    assert me.get_json()["user"]["email"] == email


def test_bearer_token_alone_authenticates_the_full_notes_contract() -> None:
    """Every notes endpoint, reached with nothing but the Authorization header -- the
    exact shape a cross-origin SPA call takes -- behaves as it does for a cookie-backed
    session."""
    issuing_client = _client()
    email = _email()
    token = issuing_client.post(
        "/api/auth/register", json={"email": email, "password": MIN_PASSWORD}
    ).get_json()["token"]
    headers = _bearer_headers(token)

    bearer_client = _client()

    created = bearer_client.post(
        "/api/notes", json={"title": "Bearer only", "body": "no cookie involved"}, headers=headers
    )
    assert created.status_code == 201
    note = created.get_json()["note"]

    listing = bearer_client.get("/api/notes", headers=headers)
    assert listing.status_code == 200
    assert any(n["id"] == note["id"] for n in listing.get_json()["notes"])

    fetched = bearer_client.get(f"/api/notes/{note['id']}", headers=headers)
    assert fetched.status_code == 200

    updated = bearer_client.put(
        f"/api/notes/{note['id']}", json={"title": "Bearer only", "body": "edited"}, headers=headers
    )
    assert updated.status_code == 200

    deleted = bearer_client.delete(f"/api/notes/{note['id']}", headers=headers)
    assert deleted.status_code in (200, 204)


def test_bearer_token_still_scopes_notes_to_the_token_owner() -> None:
    """Ownership enforcement does not depend on which auth mechanism proved identity:
    a bearer token for user A cannot reach user B's note any more than A's cookie could."""
    owner_client = _client()
    owner_token = owner_client.post(
        "/api/auth/register", json={"email": _email(), "password": MIN_PASSWORD}
    ).get_json()["token"]
    owner_note = owner_client.post(
        "/api/notes",
        json={"title": "Owner's note", "body": "private"},
        headers=_bearer_headers(owner_token),
    ).get_json()["note"]

    other_client = _client()
    other_token = other_client.post(
        "/api/auth/register", json={"email": _email(), "password": MIN_PASSWORD}
    ).get_json()["token"]

    response = other_client.get(
        f"/api/notes/{owner_note['id']}", headers=_bearer_headers(other_token)
    )
    assert response.status_code in (403, 404)


def test_missing_authorization_header_returns_401_for_a_cookie_free_client() -> None:
    client = _client()

    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/notes").status_code == 401


def test_malformed_bearer_scheme_is_rejected() -> None:
    client = _client()

    response = client.get("/api/notes", headers={"Authorization": "NotBearer something"})

    assert response.status_code == 401


def test_tampered_bearer_token_is_rejected() -> None:
    issuing_client = _client()
    token = issuing_client.post(
        "/api/auth/register", json={"email": _email(), "password": MIN_PASSWORD}
    ).get_json()["token"]
    tampered = token[:-1] + ("a" if token[-1] != "a" else "b")

    client = _client()
    response = client.get("/api/auth/me", headers=_bearer_headers(tampered))

    assert response.status_code == 401
