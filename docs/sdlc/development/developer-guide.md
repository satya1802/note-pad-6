# Developer Guide

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start status -->
_Up to date._
<!-- sdlc:auto:end status -->

<!-- sdlc:auto:start source -->
Generated from commit `e809ac9` · model `claude-sonnet-5`
<!-- sdlc:auto:end source -->

<!-- sdlc:auto:start overview -->
note pad 6 is a generated two-app repository for a simple notes product: a Vite + Svelte 5 frontend with approved, fully-built screens that currently run on seeded sample data, and a Flask 3.0 + SQLAlchemy backend that implements email/password auth (Flask-Login, bearer-token sessions) and full CRUD + search for notes scoped to the signed-in user. The backend uses SQLite locally by default and PostgreSQL 16 in deployment (docker-compose provides a local Postgres), with Flask-CORS configured for the frontend's separate origin and gunicorn as the production server.
<!-- sdlc:auto:end overview -->

<!-- sdlc:auto:start prerequisites -->
- Node.js (for npm/Vite/Svelte 5, per frontend devDependencies)
- Python 3.12 (matches backend/Dockerfile base image)
- pip
- Docker and Docker Compose (optional, for the PostgreSQL 16 service in docker-compose.yml)
<!-- sdlc:auto:end prerequisites -->

<!-- sdlc:auto:start setup -->
1. Clone the repository
2. cd backend && pip install -r requirements.txt
3. (Optional) docker compose up -d db  # starts PostgreSQL 16 on :5432; without it the backend falls back to a local SQLite file (app.db)
4. (Optional) export DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app  # point the backend at the compose Postgres instance instead of SQLite
5. (Optional) export JWT_SECRET_KEY=<secret> and ALLOWED_ORIGINS=http://localhost:5173  # sign session tokens and allow the frontend's dev origin
6. cd frontend && npm install
<!-- sdlc:auto:end setup -->

<!-- sdlc:auto:start run -->
| Name | Command | Description |
|---|---|---|
| backend dev | `cd backend && flask --app app run --debug` | Runs the Flask app factory (app.create_app) with auto-reload; creates DB tables on startup and serves /health plus the /api/auth and /api/notes routes. |
| frontend dev | `cd frontend && npm run dev` | Starts the Vite dev server for the Svelte app on the default port (5173). |
| frontend preview/build | `cd frontend && npm run build && npm run preview -- --port 4173 --host 127.0.0.1` | Builds the production bundle and serves it locally (used by Playwright's webServer config). |
| backend container | `cd backend && docker build -t notepad6-backend . && docker run -p 8000:8000 notepad6-backend` | Builds and runs the backend's Dockerfile image, which serves via gunicorn on port 8000 and exposes a /health check. |
| compose db | `docker compose up -d db` | Starts the PostgreSQL 16 database defined in docker-compose.yml with a healthcheck, persisting data to the db-data volume. |
<!-- sdlc:auto:end run -->

<!-- sdlc:auto:start structure -->
| Path | Purpose |
|---|---|
| `backend` | Flask API service: app factory, models, routes, services, tests |
| `backend/app` | Application package: __init__.py (factory), database.py, models.py, routes/, services/ |
| `backend/app/routes` | Blueprints: api.py (auth endpoints) and web_frontend.py (notes CRUD/search endpoints) |
| `backend/app/services` | Business logic: auth_service.py (register/authenticate/token signing) and notes_service.py (note CRUD/search) |
| `backend/tests` | pytest suite: health check, free-access, and integration tests (auth, CORS, notes, privacy, session token) |
| `backend/scripts` | Operational scripts, e.g. check_connections.py |
| `frontend` | Vite + Svelte 5 single-page app (the approved, generated UI) |
| `frontend/src` | App source: entry point, App.svelte shell/router, screens, and lib |
| `frontend/src/screens` | One Svelte component per approved screen (Register, SignIn, Notes, Note) with co-located tests |
| `frontend/src/lib` | api.ts (API client), session.svelte.ts, router.svelte.ts, brand.ts, and the lib/ui component vocabulary |
| `frontend/e2e` | Playwright acceptance specs (auth, notes, privacy, free-access, example) |
| `.devcontainer` | VS Code devcontainer configuration |
| `.quorq` | Platform metadata (handoff.json, prepared.json) used by the Quorq SDLC platform |
<!-- sdlc:auto:end structure -->

<!-- sdlc:auto:start conventions -->
- Backend organized as Flask blueprints per architecture component (api.py, web_frontend.py), with HTTP translation kept in routes and business logic in app/services
- SQLAlchemy models use UUID string primary keys generated in Python (uuid.uuid4) rather than DB-generated IDs
- PostgreSQL-only types (CITEXT, TSVECTOR) are given SQLite-compatible @compiles fallbacks so the same models work against the SQLite dev fallback and tests
- Authentication is bearer-token based for the cross-origin SPA (Authorization: Bearer <token>), with Flask-Login's cookie session kept only as a same-origin fallback (e.g. the test client)
- Frontend: one Svelte component per screen in src/screens, routed via a simple route table in App.svelte and src/lib/router.svelte.ts; shared UI primitives live in src/lib/ui
- Frontend tests are co-located with the components/modules they cover (*.test.ts beside the source file); Playwright specs live separately under e2e/
- Code style enforced via ESLint + Prettier (frontend) and Ruff (backend); both are treated as gates the project expects to stay green
<!-- sdlc:auto:end conventions -->

<!-- sdlc:auto:start testing -->
| Name | Command | Description |
|---|---|---|
| backend unit/integration tests | `cd backend && pytest` | Runs the pytest suite in backend/tests (health, free-access, and integration tests for auth, CORS, notes, privacy, session tokens). |
| backend lint | `cd backend && ruff check .` | Lints the backend Python code per backend/ruff.toml. |
| backend format check | `cd backend && ruff format .` | Formats backend Python code with Ruff's formatter. |
| frontend unit tests | `cd frontend && npm run test` | Runs Vitest component tests (Testing Library for Svelte) located beside the components. |
| frontend lint | `cd frontend && npm run lint` | Runs ESLint across the frontend app; this is the gate the platform runs during development. |
| frontend e2e | `cd frontend && npm run test:e2e` | Runs Playwright acceptance tests from frontend/e2e; without E2E_BASE_URL it builds/serves the frontend and starts the backend locally via Flask. |
| frontend e2e browser install | `cd frontend && npm run test:e2e:install` | Installs the Chromium browser Playwright needs before running test:e2e. |
<!-- sdlc:auto:end testing -->

<!-- sdlc:auto:start troubleshooting -->
| Problem | Solution |
|---|---|
| Frontend calls to the API fail with a CORS error in the browser console | Set ALLOWED_ORIGINS on the backend to include the frontend's origin (defaults to http://localhost:5173 and http://127.0.0.1:5173 when unset). |
| `pytest` fails with `ModuleNotFoundError: No module named 'app'` when run from elsewhere | Run pytest from the backend/ directory so pytest.ini's `pythonpath = .` puts the app package on sys.path. |
| Backend startup fails when pointed at PostgreSQL with a missing 'citext' type | The app auto-creates the citext extension on startup when the dialect is postgresql; ensure the DB user has privileges to run CREATE EXTENSION, or pre-create it manually. |
| Authenticated requests from the deployed/cross-origin frontend return 401 despite a successful login | The cross-origin SPA cannot rely on the Flask-Login session cookie; ensure the frontend stores the `token` returned by /api/auth/login or /api/auth/register (via setSessionToken) and that apiFetch sends it as `Authorization: Bearer <token>`. |
| `npm run test:e2e` hangs or fails to connect to the backend | Ensure a Python virtualenv exists at backend/.venv with dependencies installed (playwright.config.ts's webServer runs `.venv/bin/python -m flask`), or set E2E_BASE_URL to run against an already-deployed instance instead. |
| Frontend screens show the same data regardless of backend state | The approved frontend screens currently run on seeded sample data and are not yet wired to the generated backend endpoints; wiring a screen to its real endpoint is expected follow-up work, not a bug. |
<!-- sdlc:auto:end troubleshooting -->
