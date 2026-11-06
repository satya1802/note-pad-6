"""Views for API.

Endpoints the approved API spec declares without naming a component that owns them.
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from app.database import SessionLocal
from app.services.auth_service import (
    EmailAlreadyInUse,
    ValidationError,
    authenticate,
    register_user,
    serialize_user,
)

bp = Blueprint("api", __name__)


@bp.route("/api/auth/register", methods=["POST"])
def post_api_auth_register():
    """Create an account from email and password, validating format/uniqueness, then start
    a session."""
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    with SessionLocal() as session:
        try:
            user = register_user(session, email, password)
        except ValidationError as exc:
            return jsonify({"error": "validation_failed", "fields": exc.errors}), 422
        except EmailAlreadyInUse:
            return (
                jsonify({"error": "email_in_use", "message": "That email is already registered."}),
                409,
            )

        login_user(user)
        return jsonify({"user": serialize_user(user)}), 201


@bp.route("/api/auth/login", methods=["POST"])
def post_api_auth_login():
    """Authenticate email and password and start a web-managed session."""
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    with SessionLocal() as session:
        user = authenticate(session, email, password)
        if user is None:
            return (
                jsonify({"error": "invalid_credentials", "message": "Invalid email or password."}),
                401,
            )

        login_user(user)
        return jsonify({"user": serialize_user(user)}), 200


@bp.route("/api/auth/logout", methods=["POST"])
@login_required
def post_api_auth_logout():
    """End the current session."""
    logout_user()
    return jsonify({"message": "signed out"}), 200


@bp.route("/api/auth/me", methods=["GET"])
@login_required
def get_api_auth_me():
    """Return the current signed-in user or unauthenticated."""
    return jsonify({"user": serialize_user(current_user)}), 200
