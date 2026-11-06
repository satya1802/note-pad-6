"""Business logic for account registration and credential verification.

Kept out of the view layer so `app/routes/api.py` only has to translate between HTTP and
these calls.
"""

from email_validator import EmailNotValidError, validate_email
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User

MIN_PASSWORD_LENGTH = 8


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
