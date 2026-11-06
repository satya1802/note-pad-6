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


def test_ac011_get_note_returns_full_shape_for_owner() -> None:
    client = _signed_in_client()
    created = client.post("/api/notes", json={"title": "T", "body": "B"}).get_json()["note"]

    response = client.get(f"/api/notes/{created['id']}")

    assert response.status_code == 200
    note = response.get_json()["note"]
    assert note["id"] == created["id"]
    assert note["title"] == "T"
    assert note["body"] == "B"
    assert note["created_at"]
    assert note["updated_at"]


def test_ac012_get_put_delete_require_session() -> None:
    client = _signed_in_client()
    created = client.post("/api/notes", json={"title": "T", "body": "B"}).get_json()["note"]
    anon = _client()

    assert anon.get(f"/api/notes/{created['id']}").status_code == 401
    assert anon.put(f"/api/notes/{created['id']}", json={"title": "x"}).status_code == 401
    assert anon.delete(f"/api/notes/{created['id']}").status_code == 401


def test_ac012_non_owned_note_rejected_without_leaking_content(monkeypatch=None) -> None:
    owner = _signed_in_client()
    created = owner.post("/api/notes", json={"title": "Secret", "body": "Hidden body"}).get_json()[
        "note"
    ]
    other = _signed_in_client()

    get_resp = other.get(f"/api/notes/{created['id']}")
    put_resp = other.put(f"/api/notes/{created['id']}", json={"title": "hacked"})
    delete_resp = other.delete(f"/api/notes/{created['id']}")

    assert get_resp.status_code in (403, 404)
    assert put_resp.status_code in (403, 404)
    assert delete_resp.status_code in (403, 404)
    assert "Secret" not in get_resp.get_data(as_text=True)
    assert "Hidden" not in get_resp.get_data(as_text=True)

    # A bogus id that was never a UUID is rejected the same way, not a 500.
    bogus = owner.get("/api/notes/not-a-real-id")
    assert bogus.status_code in (403, 404)

    # The owner's note still exists untouched.
    still_there = owner.get(f"/api/notes/{created['id']}")
    assert still_there.status_code == 200
    assert still_there.get_json()["note"]["title"] == "Secret"


def test_ac013_put_persists_changes_and_updates_timestamp() -> None:
    client = _signed_in_client()
    created = client.post("/api/notes", json={"title": "Old", "body": "Old body"}).get_json()[
        "note"
    ]

    response = client.put(
        f"/api/notes/{created['id']}", json={"title": "New", "body": "New body"}
    )

    assert response.status_code == 200
    note = response.get_json()["note"]
    assert note["title"] == "New"
    assert note["body"] == "New body"
    assert note["created_at"] == created["created_at"]
    assert note["updated_at"] != created["updated_at"]

    fetched = client.get(f"/api/notes/{created['id']}").get_json()["note"]
    assert fetched["title"] == "New"
    assert fetched["body"] == "New body"


def test_ac014_put_with_blank_title_and_body_returns_422_and_persists_nothing() -> None:
    client = _signed_in_client()
    created = client.post("/api/notes", json={"title": "Keep", "body": "Keep body"}).get_json()[
        "note"
    ]

    response = client.put(f"/api/notes/{created['id']}", json={"title": "", "body": ""})

    assert response.status_code == 422
    body = response.get_json()
    assert "content" in body["message"].lower() or "enter" in body["message"].lower()

    unchanged = client.get(f"/api/notes/{created['id']}").get_json()["note"]
    assert unchanged["title"] == "Keep"
    assert unchanged["body"] == "Keep body"
    assert unchanged["updated_at"] == created["updated_at"]


def test_ac015_delete_removes_note_permanently() -> None:
    client = _signed_in_client()
    created = client.post("/api/notes", json={"title": "Gone", "body": "soon"}).get_json()["note"]

    response = client.delete(f"/api/notes/{created['id']}")

    assert response.status_code in (200, 204)

    listing = client.get("/api/notes").get_json()["notes"]
    assert all(n["id"] != created["id"] for n in listing)

    missing = client.get(f"/api/notes/{created['id']}")
    assert missing.status_code in (403, 404)
