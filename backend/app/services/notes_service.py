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


def list_notes(session: Session, user_id: str, q: str | None = None) -> list[Note]:
    """Return `user_id`'s notes ordered by updated_at desc.

    When `q` is non-blank, only notes whose title or body contains it (case-insensitive)
    are returned. Blank or missing `q` is an unfiltered list. Always scoped to
    `user_id`; never accepts the user id itself from the caller's untrusted input."""
    query = session.query(Note).filter(Note.user_id == user_id)
    if q and q.strip():
        term = q.strip()
        query = query.filter((Note.title.ilike(f"%{term}%")) | (Note.body.ilike(f"%{term}%")))
    return query.order_by(Note.updated_at.desc()).all()


def get_note(session: Session, user_id: str, note_id: str) -> Note | None:
    """Return the note with `note_id` if it belongs to `user_id`, else `None`."""
    try:
        return session.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    except Exception:
        session.rollback()
        return None


def update_note(
    session: Session, user_id: str, note_id: str, title: str | None, body: str | None
) -> Note | None:
    """Update title/body of `user_id`'s note `note_id`. Returns `None` if the note is
    not found or not owned. Raises `EmptyNoteError` if both title and body would end up
    blank; persists no change in that case."""
    note = get_note(session, user_id, note_id)
    if note is None:
        return None

    new_title = note.title if title is None else title.strip()
    new_body = note.body if body is None else (body or "")

    if not new_title.strip() and not new_body.strip():
        raise EmptyNoteError()

    note.title = new_title
    note.body = new_body
    note.updated_at = datetime.now(UTC)
    session.commit()
    session.refresh(note)
    return note


def delete_note(session: Session, user_id: str, note_id: str) -> bool:
    """Permanently delete `user_id`'s note `note_id`. Returns whether a row was deleted."""
    note = get_note(session, user_id, note_id)
    if note is None:
        return False
    session.delete(note)
    session.commit()
    return True


def serialize_note(note: Note) -> dict[str, str]:
    """The public shape of a note."""
    return {
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
    }
