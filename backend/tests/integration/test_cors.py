"""Integration test for the cross-origin configuration itself.

The frontend and this API are always on different origins once deployed (the SPA on one
host, the API on another -- see `app/__init__.py`'s `CORS(...)` call), so a browser will
refuse every call unless the response carries an `Access-Control-Allow-Origin` that
matches the caller's `Origin`. `ALLOWED_ORIGINS` is read once, at `create_app()` time,
so this is the one place that configuration can be proven to reach the running app --
nothing else in this suite sets it or checks the resulting header.
"""

from app import create_app


def test_configured_origin_is_echoed_back_as_allowed(monkeypatch) -> None:
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://notes.example.com")
    client = create_app().test_client()

    response = client.get("/health", headers={"Origin": "https://notes.example.com"})

    assert response.headers.get("Access-Control-Allow-Origin") == "https://notes.example.com"


def test_an_origin_not_in_allowed_origins_is_not_echoed_back(monkeypatch) -> None:
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://notes.example.com")
    client = create_app().test_client()

    response = client.get("/health", headers={"Origin": "https://evil.example.com"})

    assert response.headers.get("Access-Control-Allow-Origin") != "https://evil.example.com"


def test_allowed_origins_accepts_a_comma_separated_list(monkeypatch) -> None:
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://a.example.com, https://b.example.com")
    client = create_app().test_client()

    first = client.get("/health", headers={"Origin": "https://a.example.com"})
    second = client.get("/health", headers={"Origin": "https://b.example.com"})

    assert first.headers.get("Access-Control-Allow-Origin") == "https://a.example.com"
    assert second.headers.get("Access-Control-Allow-Origin") == "https://b.example.com"
