"""Business logic for creating and listing notes.

Kept out of the view layer so `app/routes/web_frontend.py` only has to translate
between HTTP and these calls. Every query here is scoped to a user id supplied by the
caller -- the caller is responsible for getting that id from the verified session, never
from the request body.
"""

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models import Note


class EmptyNoteError(Exception):
    """Raised when a note would be created with no title and no body content."""


def _derive_title(title: str | None, body: str) -> str:
    """Use the given title if non-blank, else the first non-blank line of the body."""
    if title and title.strip():
        return title.strip()
    for line in body.splitlines():
        if line.strip():
            return line.strip()
    return ""


def create_note(session: Session, user_id: str, title: str | None, body: str | None) -> Note:
    """Create a note for `user_id`. Raises `EmptyNoteError` if title and body are both
    blank; creates no row in that case."""
    body = body or ""
    derived_title = _derive_title(title, body)

    if not derived_title and not body.strip():
        raise EmptyNoteError()

    now = datetime.now(UTC)
    note = Note(user_id=user_id, title=derived_title, body=body, created_at=now, updated_at=now)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def list_notes(session: Session, user_id: str) -> list[Note]:
    """Return `user_id`'s notes, newest first."""
    return (
        session.query(Note).filter(Note.user_id == user_id).order_by(Note.created_at.desc()).all()
    )


def serialize_note(note: Note) -> dict[str, str]:
    """The public shape of a note."""
    return {
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
    }
