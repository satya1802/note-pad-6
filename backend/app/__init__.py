"""The application factory for note pad 6.

Generated from the approved architecture: one blueprint per component that owns
endpoints, one view per endpoint the API spec declares. Every generated view is a stub
that returns a placeholder, so the service starts and passes its tests before a single
view is implemented.
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from sqlalchemy import text

from app import models  # noqa: F401 -- imported so the tables register before create_all
from app.database import Base, SessionLocal, engine
from app.routes.api import bp as api_bp
from app.routes.web_frontend import bp as web_frontend_bp
from app.services.auth_service import verify_session_token

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> models.User | None:
    """Flask-Login's hook from a session's stored id back to a `User` row.

    Flask-Login only reaches this when a request carries its own session cookie (set by
    `login_user()`), which happens on same-origin callers such as the test client. The
    deployed frontend is cross-origin and never gets that cookie; `load_user_from_request`
    below is what authenticates it.
    """
    with SessionLocal() as session:
        return session.get(models.User, user_id)


@login_manager.request_loader
def load_user_from_request(request) -> models.User | None:  # noqa: ANN001
    """Flask-Login's fallback when a request carries no session cookie: the bearer
    token `/api/auth/login` or `/api/auth/register` returned, sent back as
    `Authorization: Bearer <token>`. This is what the deployed frontend actually uses,
    since the API and the SPA are on different origins and a cross-origin session
    cookie is not something a browser reliably keeps sending.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[len("Bearer ") :].strip()
    user_id = verify_session_token(token)
    if not user_id:
        return None
    with SessionLocal() as session:
        return session.get(models.User, user_id)


def create_app() -> Flask:
    app = Flask(__name__)

    # Signs Flask's own session cookie and any token Flask-Login related code mints.
    # This is JWT_SECRET_KEY (private), never SECRET_KEY (the public bearer the frontend
    # sends) -- signing with a value the frontend already has would let it forge sessions.
    app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-insecure-change-me")

    # The SPA runs on a different origin than the API, so the browser refuses its calls
    # unless that origin is allowed here. In development that is the Vite dev server;
    # when deployed, the platform injects the frontend's real URL as ALLOWED_ORIGINS.
    dev_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    allowed = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
    CORS(app, origins=allowed or dev_origins, supports_credentials=True)

    # The deployed frontend authenticates with the bearer token `/api/auth/login` and
    # `/api/auth/register` return (see `load_user_from_request` above), not this cookie:
    # a cross-origin browser drops a session cookie unless every attribute is exactly
    # right, and that keeps getting stricter regardless. Flask-Login still sets one as a
    # fallback for a same-origin caller (the test client here); mark it SameSite=None and
    # Secure so it at least behaves correctly if a cross-origin caller ever receives it.
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True

    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized() -> tuple[dict[str, str], int]:
        """JSON 401 rather than Flask-Login's default redirect to a login view this API
        does not have."""
        return jsonify({"error": "unauthorized", "message": "Authentication required."}), 401

    # citext (case-insensitive email) is a PostgreSQL extension, not a built-in type --
    # it has to exist in the database before create_all can create a column of that type.
    # A no-op on the SQLite fallback, where app.models compiles CITEXT down to VARCHAR.
    if engine.dialect.name == "postgresql":
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))

    # The scaffold ships no migrations, so the tables are created from the models on
    # startup. Replace this with Alembic before anything holds data worth keeping.
    Base.metadata.create_all(bind=engine)

    app.register_blueprint(api_bp)
    app.register_blueprint(web_frontend_bp)

    @app.get("/health")
    def health() -> dict[str, object]:
        """Liveness probe, and the only view here that is not a stub."""
        return {"status": "ok"}

    return app
