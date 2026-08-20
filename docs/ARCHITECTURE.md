# Architecture

## Overview

AsCO₂ is a carbon-footprint web application for French associations. It uses a single FastAPI application that:

- serves the HTML frontend and static assets;
- exposes REST endpoints for authentication, users, associations, reports, and emission-factor data;
- stores application data through SQLModel;
- uses SQLite locally and can use a Neon/PostgreSQL database in production.

The frontend is intentionally lightweight: Jinja2 templates, vanilla JavaScript, and SCSS compiled to CSS. Results are estimates and should remain traceable to their source data and units.

## Project Structure

```text
asco2/
├── backend/
│   ├── main.py                 # FastAPI app, middleware, mounts, router registration
│   ├── db.py                   # DATABASE_URL, SQLModel engine, sessions, initialization
│   ├── models.py               # SQLModel database models
│   ├── schemas.py              # Typed request/response schemas
│   ├── security.py             # Password hashing and verification
│   ├── routers/
│   │   ├── public.py           # HTML pages and public factor-listing endpoints
│   │   ├── auth.py             # Login, logout, current-user session endpoints
│   │   ├── users.py            # User creation and user endpoints
│   │   ├── associations.py     # Associations, memberships, and association reports
│   │   └── agrybalise.py       # Agribalyse CSV search and lookup adapter
│   ├── data/
│   │   └── agribalyse-31-synthese.csv
│   └── ...
├── frontend/
│   ├── templates/              # Jinja2 pages extending base.html
│   ├── js/                     # Page-specific and shared browser scripts
│   └── style/                  # SCSS source and compiled CSS
├── tests/
│   ├── conftest.py             # Test database and client fixtures
│   └── test_backend_api.py     # API and template integration tests
├── docs/ARCHITECTURE.md
├── render.yaml                 # Render deployment configuration
├── requirements.txt
├── launchapi.sh                # Local development helper
└── asco2.db                    # Local SQLite database
```

## Backend

- **Framework:** FastAPI with SQLModel.
- **Database:** `backend/db.py` reads `DATABASE_URL`; the default is the repository's `asco2.db` SQLite file. `init_db()` creates missing tables at application startup.
- **Models:** `User`, `UserSession`, `Association`, `AssociationMembership`, `Report`, `Food`, `Transport`, `Stuff`, and `Digital`.
- **Authentication:** `POST /auth/login` creates a seven-day server-side session and sets the `asco2_session` HttpOnly cookie. `get_current_user` resolves and validates that cookie for protected endpoints. Cookies are marked Secure in production.
- **Authorization:** association report reads and writes require the authenticated user to be a member of the association. Membership records also carry an `is_admin` role.
- **Reports:** reports are scoped to an association rather than exposed through a standalone reports router:
  - `GET /associations/{association_id}/reports`
  - `POST /associations/{association_id}/reports`
- **Emission factors:** the Agribalyse 3.1 CSV is stored in `backend/data/`; the `agrybalise` router isolates CSV search and lookup behavior.
- **Rendering and assets:** `public.py` renders templates, while `main.py` mounts the `frontend` directory at `/static`.
- **Development refresh:** outside production, `GET /__dev/revision` returns a revision based on watched frontend and backend file modification times. The base template polls it and reloads the page when source files change.
- **API documentation:** FastAPI exposes Swagger UI at `/docs` and the OpenAPI schema at `/openapi.json`.
- **Production:** `render.yaml` runs Uvicorn and supplies `ENV=production`, a generated `SECRET_KEY`, and an externally configured `DATABASE_URL`. Production requests sent over plain HTTP are redirected to HTTPS.

### Adding backend behavior

1. Add or update typed schemas in `backend/schemas.py`.
2. Keep database access in a router/service boundary and use `get_db` for sessions.
3. Add a focused router when the behavior is a distinct resource group.
4. Register the router in `backend/main.py`.
5. Add or update integration tests in `tests/test_backend_api.py`.

## Frontend

- **Templates:** `frontend/templates/base.html` provides the shared navbar, footer, stylesheet, favicon, and scripts. Pages extend it through Jinja2 blocks.
- **Pages:** public routes include `/`, `/login`, `/signup`, `/dashboard`, `/association/{association_id}`, and `/methodologie`.
- **Browser behavior:** `dashboard.js` loads the authenticated user's associations and links each association to its reports page. `association-page.js` loads the association metadata and its reports, handling authentication and membership errors.
- **Styles:** `style.scss` is the entry point; shared concerns live in `_variables.scss`, `_base.scss`, `_navbar.scss`, and `_footer.scss`, while page-specific styles use dedicated partials such as `_dashboard.scss` and `_home.scss`.

### Adding a page

1. Create `frontend/templates/<page>.html` and extend `base.html`.
2. Add its page route in `backend/routers/public.py`.
3. Add page-specific SCSS and import it from `frontend/style/style.scss`.
4. Add page-specific JavaScript when needed and include it in the template's `scripts` block.

## Key Conventions

- Use ADEME/Agribalyse-compatible sources and retain factor metadata where factors are exposed or used.
- Normalize units before calculations; do not hide conversion constants in route handlers.
- Keep I/O and API access separate from pure calculation logic.
- Validate user input with explicit Pydantic/SQLModel schemas.
- Do not log secrets or hard-code API keys; use environment variables.
- Preserve access control on association-scoped data.
