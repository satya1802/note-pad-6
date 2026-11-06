"""Integration tests for note creation and listing."""

import uuid

from app import create_app

MIN_PASSWORD = "correct-horse"


def _client():
    app = create_app()
    app.testing = True
    return app.test_client()


def _email() -> str:
    return f"user-{uuid.uuid4()}@example.com"


def _signed_in_client():
    client = _client()
    email = _email()
    client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})
    return client


def test_ac008_create_and_list_notes_scoped_to_session_user() -> None:
    client = _signed_in_client()

    create = client.post("/api/notes", json={"title": "My note", "body": "Some body text"})
    assert create.status_code == 201
    created = create.get_json()["note"]
    assert created["title"] == "My note"
    assert created["body"] == "Some body text"
    assert created["created_at"] == created["updated_at"]

    listing = client.get("/api/notes")
    assert listing.status_code == 200
    notes = listing.get_json()["notes"]
    assert len(notes) == 1
    assert notes[0]["id"] == created["id"]


def test_ac008_newest_first_and_other_users_never_returned() -> None:
    client_a = _signed_in_client()
    client_b = _signed_in_client()

    client_a.post("/api/notes", json={"title": "First", "body": "a"})
    client_a.post("/api/notes", json={"title": "Second", "body": "b"})
    client_b.post("/api/notes", json={"title": "Not mine", "body": "c"})

    listing = client_a.get("/api/notes")
    assert listing.status_code == 200
    notes = listing.get_json()["notes"]
    titles = [n["title"] for n in notes]
    assert titles == ["Second", "First"]
    assert "Not mine" not in titles


def test_ac009_blank_title_derives_from_first_body_line() -> None:
    client = _signed_in_client()

    response = client.post("/api/notes", json={"title": "", "body": "First line\nrest of body"})

    assert response.status_code == 201
    note = response.get_json()["note"]
    assert note["title"] == "First line"


def test_ac010_rejects_note_with_no_title_and_no_body() -> None:
    client = _signed_in_client()

    response = client.post("/api/notes", json={"title": "", "body": ""})

    assert response.status_code == 422
    body = response.get_json()
    assert "enter" in body["message"].lower()

    listing = client.get("/api/notes")
    assert listing.get_json()["notes"] == []


def test_ac_get_notes_requires_session() -> None:
    client = _client()

    response = client.get("/api/notes")

    assert response.status_code == 401


def test_ac_post_notes_requires_session() -> None:
    client = _client()

    response = client.post("/api/notes", json={"title": "x", "body": "y"})

    assert response.status_code == 401
