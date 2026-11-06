"""Business logic for account registration and credential verification.

Kept out of the view layer so `app/routes/api.py` only has to translate between HTTP and
these calls.
"""

import itsdangerous
from email_validator import EmailNotValidError, validate_email
from flask import current_app
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User

MIN_PASSWORD_LENGTH = 8

# How long a bearer token stays valid after it is issued. There is no server-side
# revocation list (that would need a table this lightweight scope does not have), so
# "signing out" is purely a client-side forget-the-token action until a token's own
# expiry catches up with it.
SESSION_TOKEN_MAX_AGE = 60 * 60 * 24 * 30  # 30 days

# A fixed, non-secret string mixed into the signature so a token minted for session
# auth can never be replayed as some other signed value this app might start minting
# with the same JWT_SECRET_KEY later.
_TOKEN_SALT = "session-token"


class ValidationError(Exception):
    """Raised with per-field messages when registration input fails validation."""

    def __init__(self, errors: dict[str, str]) -> None:
        self.errors = errors
        super().__init__("validation failed")


class EmailAlreadyInUse(Exception):
    """Raised when a registration email is already taken."""


def validate_credentials(email: str | None, password: str | None) -> str:
    """Validate email format and password length.

    Returns the normalized email on success; raises `ValidationError` with one message
    per invalid field otherwise.
    """
    errors: dict[str, str] = {}
    normalized_email = ""

    if not email or not email.strip():
        errors["email"] = "Email is required."
    else:
        try:
            normalized_email = validate_email(email, check_deliverability=False).normalized
        except EmailNotValidError:
            errors["email"] = "Email format is invalid."

    if not password:
        errors["password"] = "Password is required."
    elif len(password) < MIN_PASSWORD_LENGTH:
        errors["password"] = f"Password must be at least {MIN_PASSWORD_LENGTH} characters."

    if errors:
        raise ValidationError(errors)
    return normalized_email


def register_user(session: Session, email: str | None, password: str | None) -> User:
    """Create a new account, hashing the password. Raises `ValidationError` or
    `EmailAlreadyInUse`."""
    normalized_email = validate_credentials(email, password)

    existing = session.query(User).filter(User.email == normalized_email).first()
    if existing is not None:
        raise EmailAlreadyInUse()

    user = User(email=normalized_email, password_hash=generate_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate(session: Session, email: str | None, password: str | None) -> User | None:
    """Return the matching `User` for valid credentials, else `None`.

    Never reveals which of email/password was wrong: the caller turns `None` into one
    generic error.
    """
    if not email or not password:
        return None
    user = session.query(User).filter(User.email == email.strip()).first()
    if user is None or not check_password_hash(user.password_hash, password):
        return None
    return user


def serialize_user(user: User) -> dict[str, str]:
    """The public shape of a user: never the password hash."""
    return {"id": user.id, "email": user.email}


def generate_session_token(user: User) -> str:
    """Sign a bearer token carrying `user`'s id.

    The frontend runs on a different origin than this API once deployed, so a
    session cookie is unreliable at best (a cross-origin browser drops it unless every
    attribute is exactly right, and keeps getting stricter regardless). This token is
    what the frontend stores instead and sends back as `Authorization: Bearer <token>`
    on every later call -- signed with `JWT_SECRET_KEY` (Flask's `SECRET_KEY` config),
    never with the public `SECRET_KEY` bearer the frontend already sends, which would
    let anyone holding that public value forge a session.
    """
    serializer = itsdangerous.URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"], salt=_TOKEN_SALT
    )
    return serializer.dumps({"user_id": user.id})


def verify_session_token(token: str) -> str | None:
    """Return the user id `token` was issued for, or `None` if it is missing,
    malformed, tampered with, or older than `SESSION_TOKEN_MAX_AGE`."""
    if not token:
        return None
    serializer = itsdangerous.URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"], salt=_TOKEN_SALT
    )
    try:
        data = serializer.loads(token, max_age=SESSION_TOKEN_MAX_AGE)
    except itsdangerous.BadData:
        return None
    user_id = data.get("user_id") if isinstance(data, dict) else None
    return user_id if isinstance(user_id, str) else None
