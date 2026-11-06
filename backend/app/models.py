"""SQLAlchemy models for the approved data model.

Two tables: `users` (an account, with a hashed password) and `notes` (owned by exactly one
user, searched by `search_tsv`). The base is bound to the engine in `app.database`; this
module only has to be imported once, which `app/__init__.py` already does, before
`Base.metadata.create_all` runs.

`CITEXT` (case-insensitive email, so "A@b.com" and "a@b.com" collide the way a login form
needs) and `TSVECTOR` (the full-text search column) are PostgreSQL-only types. The
`@compiles` registrations below give them a plain fallback so the same models also create a
working schema on the SQLite database `app.database` falls back to when `DATABASE_URL` is
not set (a fresh clone, or the unit-test run) -- without that, `create_all` raises on SQLite
before a single test runs. Deployed, `DATABASE_URL` points at the real PostgreSQL, where the
native types apply and full-text search is wired up by the migration/application code that
populates `search_tsv` -- that behaviour is not scaffolded here.
"""

import uuid
from datetime import UTC, datetime

from flask_login import UserMixin
from sqlalchemy import DateTime, ForeignKey, Text, Uuid
from sqlalchemy.dialects.postgresql import CITEXT, TSVECTOR
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


@compiles(CITEXT, "sqlite")
def _citext_as_varchar(element: CITEXT, compiler, **kw) -> str:  # noqa: ANN001
    return "VARCHAR COLLATE NOCASE"


@compiles(TSVECTOR, "sqlite")
def _tsvector_as_text(element: TSVECTOR, compiler, **kw) -> str:  # noqa: ANN001
    return "TEXT"


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(UTC)


class User(Base, UserMixin):
    """An account. `UserMixin` gives Flask-Login the `is_authenticated` /
    `get_id` surface a session-protected view needs."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=_new_uuid)
    email: Mapped[str] = mapped_column(CITEXT, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    notes: Mapped[list["Note"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Note(Base):
    """A note, owned by exactly one user. `search_tsv` backs the full-text search over a
    user's own notes; populating and indexing it is left to the code that implements
    `GET /api/notes?q=`."""

    __tablename__ = "notes"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(Text, nullable=False, default="")
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    search_tsv: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="notes")


__all__ = ["Base", "Note", "User"]
