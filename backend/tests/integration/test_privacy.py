"""Integration tests proving one user's notes are never exposed to, or changed by,
another signed-in user (AC-022, AC-023), and that every /api/notes endpoint requires
an active session."""

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


def test_ac022_list_search_get_put_delete_never_touch_other_users_notes() -> None:
    a = _signed_in_client()
    b = _signed_in_client()

    a_note = a.post("/api/notes", json={"title": "A's secret plan", "body": "only A should see"}).get_json()[
        "note"
    ]
    b_note = b.post(
        "/api/notes", json={"title": "B's secret plan", "body": "only B should see"}
    ).get_json()["note"]

    # list: A never sees B's note, and vice versa.
    a_list = [n["id"] for n in a.get("/api/notes").get_json()["notes"]]
    b_list = [n["id"] for n in b.get("/api/notes").get_json()["notes"]]
    assert b_note["id"] not in a_list
    assert a_note["id"] not in b_list

    # search: a query matching B's content returns nothing for A.
    a_search = a.get("/api/notes?q=secret").get_json()["notes"]
    assert all(n["id"] != b_note["id"] for n in a_search)
    assert all("B's secret plan" != n["title"] for n in a_search)

    # GET/PUT/DELETE of B's id from A's session: no effect on B's note.
    a.get(f"/api/notes/{b_note['id']}")
    a.put(f"/api/notes/{b_note['id']}", json={"title": "tampered", "body": "tampered"})
    a.delete(f"/api/notes/{b_note['id']}")

    still_b = b.get(f"/api/notes/{b_note['id']}")
    assert still_b.status_code == 200
    unchanged = still_b.get_json()["note"]
    assert unchanged["title"] == "B's secret plan"
    assert unchanged["body"] == "only B should see"


def test_ac023_get_put_delete_of_other_users_note_id_returns_404_without_leaking() -> None:
    owner = _signed_in_client()
    attacker = _signed_in_client()

    created = owner.post(
        "/api/notes", json={"title": "Owner Only Title", "body": "Owner only body text"}
    ).get_json()["note"]

    get_resp = attacker.get(f"/api/notes/{created['id']}")
    put_resp = attacker.put(f"/api/notes/{created['id']}", json={"title": "x", "body": "y"})
    delete_resp = attacker.delete(f"/api/notes/{created['id']}")

    assert get_resp.status_code == 404
    assert put_resp.status_code == 404
    assert delete_resp.status_code == 404

    for resp in (get_resp, put_resp, delete_resp):
        text = resp.get_data(as_text=True)
        assert "Owner Only Title" not in text
        assert "Owner only body text" not in text

    # The owner's note survives every attack attempt untouched.
    still_there = owner.get(f"/api/notes/{created['id']}")
    assert still_there.status_code == 200
    note = still_there.get_json()["note"]
    assert note["title"] == "Owner Only Title"
    assert note["body"] == "Owner only body text"


def test_all_five_notes_endpoints_return_401_without_active_session() -> None:
    owner = _signed_in_client()
    created = owner.post("/api/notes", json={"title": "T", "body": "B"}).get_json()["note"]
    anon = _client()

    assert anon.get("/api/notes").status_code == 401
    assert anon.post("/api/notes", json={"title": "x", "body": "y"}).status_code == 401
    assert anon.get(f"/api/notes/{created['id']}").status_code == 401
    assert anon.put(f"/api/notes/{created['id']}", json={"title": "x"}).status_code == 401
    assert anon.delete(f"/api/notes/{created['id']}").status_code == 401
