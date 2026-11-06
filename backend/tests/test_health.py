"""The baseline tests the scaffold ships with.

The platform installs this tree and runs `pytest` against it, so there has to be
something green to run before an agent has written anything.
"""

from app import create_app

client = create_app().test_client()


def test_health_reports_ok() -> None:
    """A failure here means the application does not import or does not start."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_every_generated_route_is_registered() -> None:
    """Every endpoint the API spec declares is wired to a view that imports."""
    rules = {rule.rule for rule in client.application.url_map.iter_rules()}
    assert "/health" in rules
