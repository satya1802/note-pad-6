# Developer Guide

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start status -->
_Up to date._
<!-- sdlc:auto:end status -->

<!-- sdlc:auto:start source -->
Generated from commit `0d3c142` · model `claude-sonnet-5`
<!-- sdlc:auto:end source -->

<!-- sdlc:auto:start overview -->
note pad 6 is a generated two-app repository for a simple notes product: a Svelte 5 + Vite frontend with every screen approved and running on seeded sample data, and a Flask 3.0 backend that implements SQLAlchemy models (User, Note) and the auth endpoints (register/login/logout/me) plus list/create notes, while the single-note GET/PUT/DELETE endpoints are still stubs returning 'not implemented'. The backend defaults to a local SQLite file so it runs with no setup, and switches to PostgreSQL 16 (the approved database) via DATABASE_URL; a docker-compose file provides a local Postgres container for that purpose.
<!-- sdlc:auto:end overview -->

<!-- sdlc:auto:start prerequisites -->
- Node.js (for Vite 6 / Svelte 5 frontend tooling)
- Python 3.12 (matches backend/Dockerfile)
- pip
- Docker and docker-compose (optional, for a local PostgreSQL 16 database)
<!-- sdlc:auto:end prerequisites -->

<!-- sdlc:auto:start setup -->
1. Clone the repository
2. cd frontend && npm install
3. cd backend && pip install -r requirements.txt
4. (optional) from the repo root run: docker-compose up -d  # starts a local PostgreSQL 16 container
5. (optional) set DATABASE_URL to point the backend at that Postgres instance; without it the backend falls back to a local sqlite:///./app.db file
<!-- sdlc:auto:end setup -->

<!-- sdlc:auto:start run -->
| Name | Command | Description |
|---|---|---|
| frontend dev | `npm run dev` | Starts the Vite dev server for the Svelte frontend |
| frontend build | `npm run build` | Bundles the frontend app (does not typecheck) |
| frontend preview | `npm run preview` | Serves the built frontend locally |
| backend dev | `flask --app app run --debug` | Runs the Flask backend in debug mode (from backend/) |
| backend prod (container) | `gunicorn app:create_app() --bind 0.0.0.0:8000` | Production entrypoint used by backend/Dockerfile |
| db | `docker-compose up -d` | Starts the PostgreSQL 16 service defined in docker-compose.yml |
<!-- sdlc:auto:end run -->

<!-- sdlc:auto:start structure -->
| Path | Purpose |
|---|---|
| `.devcontainer` | VS Code devcontainer configuration |
| `.quorq` | Platform metadata (handoff/prepared state), not application code |
| `backend` | Flask API service: app factory, models, routes, services, tests |
| `backend/app` | Application package: factory (__init__.py), database engine/session, SQLAlchemy models, stub helper |
| `backend/app/routes` | Blueprints: api.py (auth endpoints) and web_frontend.py (notes endpoints) |
| `backend/app/services` | Business logic for auth and notes used by the route handlers |
| `backend/tests` | pytest suite: health check and integration tests for auth and notes |
| `backend/scripts` | Operational scripts, e.g. checking service connections |
| `frontend` | Vite + Svelte 5 single-page app, the approved UI |
| `frontend/src` | App source: main.ts entry, App.svelte shell/router wiring, index.css |
| `frontend/src/lib` | API client (api.ts), router, session state, brand tokens, and the lib/ui component/icon vocabulary |
| `frontend/src/screens` | One Svelte component per approved screen (Register, SignIn, Notes, Note) with co-located tests |
| `frontend/e2e` | Playwright end-to-end specs |
<!-- sdlc:auto:end structure -->

<!-- sdlc:auto:start conventions -->
- Backend routes are organized as Flask blueprints per architecture component (api.py for auth, web_frontend.py for notes), each view documented with a one-line docstring describing its intended behavior
- Unimplemented endpoints return a placeholder via app/stubs.py's not_implemented() rather than being omitted
- Business logic lives in backend/app/services/*, separate from the thin route handlers in backend/app/routes/*
- SQLAlchemy models use @compiles to provide SQLite fallbacks (CITEXT, TSVECTOR) for PostgreSQL-only types, so the same models work locally on SQLite and in production on Postgres
- Frontend: one Svelte component per approved screen under src/screens, a shared UI/icon vocabulary under src/lib/ui, and a minimal custom router (src/lib/router.svelte.ts) driving App.svelte's route table
- Frontend API calls go through the single apiFetch helper in src/lib/api.ts, which attaches a session token or shared secret bearer and includes credentials for the cross-origin session cookie
- Linting/formatting enforced via ESLint+Prettier (frontend) and Ruff (backend, config in backend/ruff.toml)
<!-- sdlc:auto:end conventions -->

<!-- sdlc:auto:start testing -->
| Name | Command | Description |
|---|---|---|
| frontend unit | `npm run test` | Runs Vitest component tests under src/ with Testing Library |
| frontend lint | `npm run lint` | Runs ESLint over the frontend app (gate used by the platform) |
| frontend typecheck | `npm run typecheck` | Runs svelte-check over the TypeScript in the frontend |
| frontend e2e | `npm run test:e2e` | Runs Playwright acceptance tests from e2e/; builds/serves the frontend and starts the backend automatically unless E2E_BASE_URL is set |
| backend tests | `pytest` | Runs the backend test suite (health check and auth/notes integration tests) |
| backend lint | `ruff check .` | Lints the backend with Ruff |
| backend format check | `ruff format .` | Formats/checks backend code style with Ruff |
<!-- sdlc:auto:end testing -->

<!-- sdlc:auto:start troubleshooting -->
| Problem | Solution |
|---|---|
| Frontend calls to the backend fail with a CORS error | Set ALLOWED_ORIGINS on the backend to include the frontend's origin; app/__init__.py defaults to the Vite dev server origins (http://localhost:5173, http://127.0.0.1:5173) only |
| Note detail/edit/delete requests return a 'not implemented' placeholder | GET/PUT/DELETE /api/notes/{id} in backend/app/routes/web_frontend.py are stubs; only list and create notes are implemented so far |
| `pytest` from backend/ fails with ModuleNotFoundError: app | Run pytest from the backend/ directory where pytest.ini sets pythonpath = ., or always invoke it from that directory |
| Backend fails to create the citext extension | This only runs when DATABASE_URL points at PostgreSQL; ensure the Postgres user has permission to CREATE EXTENSION, or omit DATABASE_URL to use the SQLite fallback |
| Playwright e2e run can't start the backend | playwright.config.ts's webServer expects a virtualenv at backend/.venv with dependencies installed (.venv/bin/python -m flask ...); create that venv and pip install -r backend/requirements.txt into it before running npm run test:e2e locally |
<!-- sdlc:auto:end troubleshooting -->
