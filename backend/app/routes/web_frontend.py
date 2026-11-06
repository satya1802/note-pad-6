"""Views for Svelte Notes Web App.

Responsive browser UI for registration, sign-in/out, notes list, note
view/create/edit/delete, and search. Calls the backend JSON API and renders results.

Every view is a stub returning a placeholder. The shape comes from the approved
API spec; the behaviour does not exist yet.
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.database import SessionLocal
from app.services.notes_service import (
    EmptyNoteError,
    create_note,
    delete_note,
    get_note,
    list_notes,
    serialize_note,
    update_note,
)

bp = Blueprint("web_frontend", __name__)


@bp.route("/api/notes", methods=["GET"])
@login_required
def get_api_notes() -> dict[str, object]:
    """List the current user's notes ordered by created_at desc; when q is present,
    full-text search title and body of only the user's notes."""
    with SessionLocal() as session:
        notes = list_notes(session, current_user.id)
        return jsonify({"notes": [serialize_note(note) for note in notes]}), 200


@bp.route("/api/notes", methods=["POST"])
@login_required
def post_api_notes() -> dict[str, object]:
    """Create a note for the current user; derive title from first body line if
    blank and reject a fully empty note."""
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    body = data.get("body")

    with SessionLocal() as session:
        try:
            note = create_note(session, current_user.id, title, body)
        except EmptyNoteError:
            return (
                jsonify(
                    {
                        "error": "empty_note",
                        "message": "Enter a title or some body text to save a note.",
                    }
                ),
                422,
            )

        return jsonify({"note": serialize_note(note)}), 201


@bp.route("/api/notes/<id>", methods=["GET"])
@login_required
def get_api_notes_by_id(id: str) -> tuple[dict[str, object], int]:
    """Return a single note with full body and timestamps only if it belongs to the current user."""
    with SessionLocal() as session:
        note = get_note(session, current_user.id, id)
        if note is None:
            return jsonify({"error": "not_found", "message": "Note not found."}), 404
        return jsonify({"note": serialize_note(note)}), 200


@bp.route("/api/notes/<id>", methods=["PUT"])
@login_required
def put_api_notes_by_id(id: str) -> tuple[dict[str, object], int]:
    """Update title/body of the user's own note and set updated_at; reject if both become empty."""
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    body = data.get("body")

    with SessionLocal() as session:
        try:
            note = update_note(session, current_user.id, id, title, body)
        except EmptyNoteError:
            return (
                jsonify(
                    {
                        "error": "empty_note",
                        "message": "Enter a title or some body text to save a note.",
                    }
                ),
                422,
            )

        if note is None:
            return jsonify({"error": "not_found", "message": "Note not found."}), 404
        return jsonify({"note": serialize_note(note)}), 200


@bp.route("/api/notes/<id>", methods=["DELETE"])
@login_required
def delete_api_notes_by_id(id: str) -> tuple[dict[str, object] | str, int]:
    """Permanently delete the user's own note."""
    with SessionLocal() as session:
        deleted = delete_note(session, current_user.id, id)
        if not deleted:
            return jsonify({"error": "not_found", "message": "Note not found."}), 404
        return "", 204
