"""Views for API.

Endpoints the approved API spec declares without naming a component that owns them.

Every view is a stub returning a placeholder. The shape comes from the approved
API spec; the behaviour does not exist yet.
"""

from flask import Blueprint

from app.stubs import not_implemented

bp = Blueprint("api", __name__)


@bp.route("/api/auth/register", methods=["POST"])
def post_api_auth_register() -> dict[str, str]:
    """Create an account from email and password, validating format/uniqueness, then start
    a session."""
    return not_implemented("POST /api/auth/register")


@bp.route("/api/auth/login", methods=["POST"])
def post_api_auth_login() -> dict[str, str]:
    """Authenticate email and password and start a web-managed session."""
    return not_implemented("POST /api/auth/login")


@bp.route("/api/auth/logout", methods=["POST"])
def post_api_auth_logout() -> dict[str, str]:
    """End the current session."""
    return not_implemented("POST /api/auth/logout")


@bp.route("/api/auth/me", methods=["GET"])
def get_api_auth_me() -> dict[str, str]:
    """Return the current signed-in user or unauthenticated."""
    return not_implemented("GET /api/auth/me")
