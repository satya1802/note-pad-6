"""Engine and session factory.

SQLite by default so a fresh clone runs with nothing but `pip install -r
requirements.txt` -- point `DATABASE_URL` at the real database when it exists;
nothing else has to change.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite rejects a connection made on one thread and used on another, which is what
# happens when a threaded server hands requests to worker threads.
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Declarative base that every generated model inherits."""
