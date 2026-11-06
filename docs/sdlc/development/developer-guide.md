# Developer Guide

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start status -->
_Up to date._
<!-- sdlc:auto:end status -->

<!-- sdlc:auto:start source -->
Generated from commit `3f7a9df` · model `claude-sonnet-5`
<!-- sdlc:auto:end source -->

<!-- sdlc:auto:start overview -->
note pad 6 is a generated two-app repository from the Quorq AI SDLC platform: a Svelte 5 + Vite frontend that renders every approved screen against seeded sample data, and a Flask 3.0 backend that is currently just a scaffold exposing a single health check (no architecture had been approved yet, so no models or routes exist beyond stubs). The approved stack targets PostgreSQL 16 on AWS in production, but locally the backend defaults to a SQLite file and the frontend talks to a local backend URL, so the whole thing runs with no external services required.
<!-- sdlc:auto:end overview -->

<!-- sdlc:auto:start prerequisites -->
- Node.js (for npm, Vite 6, Svelte 5 tooling)
- Python 3.12
- pip
- Docker and docker-compose (optional, for a local Postgres instead of SQLite)
<!-- sdlc:auto:end prerequisites -->

<!-- sdlc:auto:start setup -->
1. Clone the repository
2. Backend: cd backend && pip install -r requirements.txt
3. (Optional) Copy .env.example to .env and set DATABASE_URL to point at a real Postgres instance; otherwise the backend falls back to a local SQLite file
4. (Optional) Start a local Postgres with: docker-compose up db
5. Frontend: cd frontend && npm install
<!-- sdlc:auto:end setup -->

<!-- sdlc:auto:start run -->
| Name | Command | Description |
|---|---|---|
| backend dev | `flask --app app run --debug` | Runs the Flask backend (app factory in backend/app/__init__.py) with debug reload; serves GET /health |
| frontend dev | `npm run dev` | Starts the Vite dev server for the Svelte 5 frontend |
| frontend build | `npm run build` | Bundles the frontend with Vite (does not typecheck) |
| frontend preview | `npm run preview` | Serves the built frontend bundle locally |
| db up | `docker-compose up db` | Starts a local PostgreSQL 16 container defined in docker-compose.yml |
<!-- sdlc:auto:end run -->

<!-- sdlc:auto:start structure -->
| Path | Purpose |
|---|---|
| `backend` | Flask API service: app factory, CORS setup, SQLAlchemy engine/session, models, and route blueprints |
| `backend/app` | Application package: __init__.py (app factory + /health route), database.py (engine/session), models.py (SQLAlchemy Base, currently no tables), routes/ (empty blueprint package, one per architecture component once endpoints are defined) |
| `backend/tests` | Pytest test suite, currently covering the health endpoint |
| `frontend` | Vite + Svelte 5 SPA containing all approved screens, UI components, and the API client seam |
| `frontend/src` | Application source: main.ts entry point, index.css, lib/ (router, API client, UI component vocabulary), test-setup.ts for Vitest |
| `frontend/e2e` | Playwright end-to-end specs run against a locally built app or a deployed URL via E2E_BASE_URL |
| `.devcontainer` | VS Code devcontainer configuration for a consistent dev environment |
| `.quorq` | Quorq platform metadata (handoff.json) describing how this repo was generated |
<!-- sdlc:auto:end structure -->

<!-- sdlc:auto:start conventions -->
- Backend uses the Flask application-factory pattern (create_app) in backend/app/__init__.py
- One Flask blueprint per architecture component that owns endpoints, under backend/app/routes/; generated views start as stubs before implementation
- SQLAlchemy models all inherit the shared Base declared in backend/app/database.py; tables are created via Base.metadata.create_all on startup (no migrations yet)
- Backend config (DATABASE_URL, ALLOWED_ORIGINS) is read from environment variables with sensible local defaults
- Frontend components live under frontend/src/lib/ui/ as the shared component/icon vocabulary; path alias @ maps to frontend/src
- Frontend API access is centralized in frontend/src/lib/api.ts (apiFetch) with bearer-token auth support, but generated screens currently render seeded sample data rather than calling it
- Frontend component tests are colocated with the components they test and run via Vitest in jsdom; Playwright specs live separately in e2e/
<!-- sdlc:auto:end conventions -->

<!-- sdlc:auto:start testing -->
| Name | Command | Description |
|---|---|---|
| frontend unit tests | `npm test` | Runs Vitest component tests (Testing Library for Svelte) under src/ |
| frontend lint | `npm run lint` | Runs ESLint over the frontend app (gate during development) |
| frontend typecheck | `npm run typecheck` | Runs svelte-check over the TypeScript around the Svelte components |
| frontend e2e | `npm run test:e2e` | Runs Playwright acceptance tests from frontend/e2e; builds/serves the app locally unless E2E_BASE_URL is set |
| frontend e2e browser install | `npm run test:e2e:install` | Installs the Chromium browser Playwright needs |
| backend tests | `pytest` | Runs the backend test suite (currently the health check) with pytest |
| backend lint | `ruff check .` | Lints the backend Python code with Ruff |
| backend format | `ruff format .` | Formats the backend Python code with Ruff |
<!-- sdlc:auto:end testing -->

<!-- sdlc:auto:start troubleshooting -->
| Problem | Solution |
|---|---|
| Frontend requests to the backend fail with a CORS error | Ensure the backend is running on one of the allowed dev origins (http://localhost:5173 or http://127.0.0.1:5173) or set ALLOWED_ORIGINS to include the frontend's URL |
| Backend import error 'cannot import app' when running pytest from an unexpected directory | Run pytest from backend/ so pytest.ini's pythonpath = . is honored, or run via `cd backend && pytest` |
| Playwright e2e tests fail to start the backend | The Playwright config expects a Python venv at backend/.venv with flask installed (`.venv/bin/python -m flask --app app run`); create that venv and install backend/requirements.txt before running npm run test:e2e locally without E2E_BASE_URL |
| Database connection fails against Postgres | Start the local database with `docker-compose up db` and set DATABASE_URL (e.g. postgresql+psycopg://app:app@localhost:5432/app) before starting the backend; otherwise it silently falls back to a local SQLite file |
<!-- sdlc:auto:end troubleshooting -->
