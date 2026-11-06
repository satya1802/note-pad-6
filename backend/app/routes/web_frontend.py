"""Views for Svelte Notes Web App.

Responsive browser UI for registration, sign-in/out, notes list, note
view/create/edit/delete, and search. Calls the backend JSON API and renders results.

Every view is a stub returning a placeholder. The shape comes from the approved
API spec; the behaviour does not exist yet.
"""

from flask import Blueprint

from app.stubs import not_implemented

bp = Blueprint("web_frontend", __name__)


@bp.route("/api/notes", methods=["GET"])
def get_api_notes() -> dict[str, str]:
    """List the current user's notes ordered by updated_at desc; when q is present,
    full-text search title and body of only the user's notes."""
    return not_implemented("GET /api/notes")


@bp.route("/api/notes", methods=["POST"])
def post_api_notes() -> dict[str, str]:
    """Create a note for the current user; derive title from first body line if
    blank and reject a fully empty note."""
    return not_implemented("POST /api/notes")


@bp.route("/api/notes/<id>", methods=["GET"])
def get_api_notes_by_id(id: str) -> dict[str, str]:
    """Return a single note with full body and timestamps only if it belongs to the current user."""
    return not_implemented("GET /api/notes/{id}")


@bp.route("/api/notes/<id>", methods=["PUT"])
def put_api_notes_by_id(id: str) -> dict[str, str]:
    """Update title/body of the user's own note and set updated_at; reject if both become empty."""
    return not_implemented("PUT /api/notes/{id}")


@bp.route("/api/notes/<id>", methods=["DELETE"])
def delete_api_notes_by_id(id: str) -> dict[str, str]:
    """Permanently delete the user's own note."""
    return not_implemented("DELETE /api/notes/{id}")
