"""The application factory for note pad 6.

Generated from the approved architecture: one blueprint per component that owns
endpoints, one view per endpoint the API spec declares. Every generated view is a stub
that returns a placeholder, so the service starts and passes its tests before a single
view is implemented.
"""

import os

from flask import Flask
from flask_cors import CORS

from app import models  # noqa: F401 -- imported so the tables register before create_all
from app.database import Base, engine


def create_app() -> Flask:
    app = Flask(__name__)

    # The SPA runs on a different origin than the API, so the browser refuses its calls
    # unless that origin is allowed here. In development that is the Vite dev server;
    # when deployed, the platform injects the frontend's real URL as ALLOWED_ORIGINS.
    dev_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    allowed = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
    CORS(app, origins=allowed or dev_origins, supports_credentials=True)

    # The scaffold ships no migrations, so the tables are created from the models on
    # startup. Replace this with Alembic before anything holds data worth keeping.
    Base.metadata.create_all(bind=engine)


    @app.get("/health")
    def health() -> dict[str, object]:
        """Liveness probe, and the only view here that is not a stub."""
        return {"status": "ok"}

    return app
