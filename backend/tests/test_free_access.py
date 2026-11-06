"""US-011 / AC-024 -- using the app (registration, sign-in, and every note feature) never
asks for payment, billing details, or a subscription upgrade.

This is an integration test over the whole API contract rather than one unit: it walks the
full registration -> sign-in -> note CRUD -> search -> sign-out path the other suites cover
piecemeal, and checks the one thing none of them assert -- that nothing in that path is, or
looks like, a payment gate. A 402 Payment Required anywhere in the flow, or a billing-shaped
key or message in a response body, fails it.
"""

import uuid

from app import create_app

MIN_PASSWORD = "correct-horse"

# Words that would only appear if a payment gate had crept into a response: a monetary
# amount field, a plan/tier name, or copy nudging the user to pay or upgrade.
FORBIDDEN_WORDS = (
    "payment",
    "billing",
    "subscription",
    "upgrade",
    "credit card",
    "card_number",
    "stripe",
    "checkout",
    "invoice",
    "trial",
    "paywall",
    "price",
)


def _client():
    app = create_app()
    app.testing = True
    return app.test_client()


def _email() -> str:
    return f"user-{uuid.uuid4()}@example.com"


def _assert_clean(response) -> None:
    """No 402, and no payment-shaped vocabulary anywhere in the response body."""
    assert response.status_code != 402
    text = response.get_data(as_text=True).lower()
    for word in FORBIDDEN_WORDS:
        assert word not in text, f"found {word!r} in response: {text}"


def test_ac024_registration_never_mentions_or_requires_payment() -> None:
    client = _client()
    email = _email()

    response = client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})

    assert response.status_code == 201
    _assert_clean(response)


def test_ac024_sign_in_sign_out_never_mentions_or_requires_payment() -> None:
    client = _client()
    email = _email()
    client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})
    client.post("/api/auth/logout")

    login = client.post("/api/auth/login", json={"email": email, "password": MIN_PASSWORD})
    assert login.status_code == 200
    _assert_clean(login)

    me = client.get("/api/auth/me")
    assert me.status_code == 200
    _assert_clean(me)

    logout = client.post("/api/auth/logout")
    assert logout.status_code == 200
    _assert_clean(logout)


def test_ac024_full_note_lifecycle_never_mentions_or_requires_payment() -> None:
    """Register, then exercise every note feature the spec declares -- create, list,
    search, read, update, delete -- checking at each step that the response is clean."""
    client = _client()
    email = _email()
    register = client.post("/api/auth/register", json={"email": email, "password": MIN_PASSWORD})
    _assert_clean(register)

    created = client.post("/api/notes", json={"title": "Weekly budget", "body": "groceries, rent"})
    assert created.status_code == 201
    _assert_clean(created)
    note_id = created.get_json()["note"]["id"]

    listing = client.get("/api/notes")
    assert listing.status_code == 200
    _assert_clean(listing)

    searched = client.get("/api/notes?q=budget")
    assert searched.status_code == 200
    _assert_clean(searched)

    fetched = client.get(f"/api/notes/{note_id}")
    assert fetched.status_code == 200
    _assert_clean(fetched)

    updated = client.put(f"/api/notes/{note_id}", json={"title": "Weekly budget", "body": "rent"})
    assert updated.status_code == 200
    _assert_clean(updated)

    deleted = client.delete(f"/api/notes/{note_id}")
    assert deleted.status_code in (200, 204)
    _assert_clean(deleted)


def test_ac024_no_billing_or_subscription_endpoint_exists() -> None:
    """There is no payment surface to hit in the first place: none of the plausible
    billing-style routes resolve to anything (a registered Flask view, even one that
    later rejects the request, would not 404)."""
    client = _client()
    client.post("/api/auth/register", json={"email": _email(), "password": MIN_PASSWORD})

    for path in (
        "/api/billing",
        "/api/billing/portal",
        "/api/subscription",
        "/api/subscriptions",
        "/api/payment",
        "/api/payments",
        "/api/checkout",
        "/api/upgrade",
        "/api/plans",
    ):
        response = client.get(path)
        assert response.status_code == 404, f"{path} resolved with {response.status_code}"
