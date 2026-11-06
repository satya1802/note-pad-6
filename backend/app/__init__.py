"""The application factory for note pad 6.

Generated from the approved architecture: one blueprint per component that owns
endpoints, one view per endpoint the API spec declares. Every generated view is a stub
that returns a placeholder, so the service starts and passes its tests before a single
view is implemented.
"""

import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from sqlalchemy import text

from app import models  # noqa: F401 -- imported so the tables register before create_all
from app.database import Base, SessionLocal, engine
from app.routes.api import bp as api_bp
from app.routes.web_frontend import bp as web_frontend_bp

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> models.User | None:
    """Flask-Login's hook from a session's stored id back to a `User` row.

    Plain id lookup only: this scaffold does not decide how a session is represented
    (cookie, bearer token, or otherwise) -- the ticket that implements login does, and
    calls `login_user()` with whatever `User` it has already authenticated.
    """
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

    login_manager.init_app(app)

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
