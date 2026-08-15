# Architecture

## Overview

AsCO₂ is a carbon-footprint web application for French associations.  
It follows a classic client/server split: a **FastAPI backend** exposes REST APIs, renders HTML templates, and serves static assets backed by SQLite.

---

## Project Structure

```
asco2/
├── backend/               # FastAPI application
│   ├── main.py            # App entry point, router registration
│   ├── db.py              # SQLite engine & session (SQLModel)
│   ├── models.py          # ORM table models
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── routers/           # One file per resource group
│   │   ├── public.py      # GET / emission factor listings (food, transport, stuff, digital)
│   │   ├── users.py       # GET/POST /users
│   │   ├── associations.py# GET/POST /associations + members
│   │   ├── reports.py     # GET/POST /reports
│   │   └── agrybalise.py  # GET /agrybalise — Agribalyse CSV adapter
│   └── data/
│       └── agribalyse-31-synthese.csv  # Local ADEME/Agribalyse emission factors
├── frontend/              # Vanilla template/static frontend
│   ├── templates/
│   │   ├── base.html      # Shared layout (navbar, footer, common assets)
│   │   ├── index.html     # Home page template
│   │   ├── login.html     # Login page template
│   │   ├── signup.html    # Signup page template
│   │   └── methodologie.html # Methodology page template
│   ├── js/
│   │   ├── navbar.js      # Burger menu toggle (shared across all pages)
│   │   └── main.js        # Home page scripts
│   └── style/
│       ├── style.scss     # Entry point — imports only
│       ├── _variables.scss# Color tokens (shared)
│       ├── _base.scss     # Reset, body, background (shared)
│       ├── _navbar.scss   # Navbar + burger menu (shared)
│       ├── _footer.scss   # Footer (shared)
│       └── _home.scss     # Hero section, buttons (page-specific)
├── tests/
│   ├── conftest.py        # Pytest fixtures (test DB, test client)
│   └── test_backend_api.py# API integration tests
├── docs/
│   └── ARCHITECTURE.md
├── requirements.txt
├── launchapi.sh           # Dev helper to start uvicorn
└── asco2.db               # SQLite database (dev)
```

---

## Backend

- **Framework:** FastAPI with SQLModel (SQLAlchemy + Pydantic).
- **Database:** SQLite (`asco2.db`), managed via SQLModel sessions.
- **Rendering:** Jinja2 templates via `backend/routers/public.py`; static files mounted at `/static` in `backend/main.py`.
- **Data models:** `User`, `Association`, `AssociationMembership`, `Report`, `Food`, `Transport`, `Stuff`, `Digital`.
- **Emission factors:** Agribalyse 3.1 CSV loaded locally in `backend/data/`. The `/agrybalise` router exposes search and lookup endpoints over it.
- **API docs:** available at `/docs` (Swagger UI) when the server is running.

### Adding a new page's backend logic
1. Create `backend/routers/<feature>.py` with an `APIRouter`.
2. Add schemas to `backend/schemas.py` if needed.
3. Register the router in `backend/main.py` with `app.include_router(...)`.

---

## Frontend

- **Stack:** Jinja2 templates + vanilla JS + SCSS (compiled to CSS) — no frontend framework.
- **Shared components:** navbar, footer, and common assets are centralized in `frontend/templates/base.html`.
- **SCSS partials:** `_variables.scss`, `_base.scss`, `_navbar.scss`, and `_footer.scss` are shared. Each page can keep its own partial (e.g., `_home.scss`) imported in `style.scss`.

### Adding a new page
1. Create `frontend/templates/<page>.html` and extend `base.html`.
2. Add a route in `backend/routers/public.py` returning `templates.TemplateResponse(...)`.
3. Create `frontend/style/_<page>.scss` for page-specific styles; add `@import "<page>"` in `style.scss`.
4. Create `frontend/js/<page>.js` for page-specific scripts if needed, then include it in the template `scripts` block.

---

## Key Conventions

- All emission factor constants must be traceable to their source (ADEME/Agribalyse).
- Units must be normalized before any calculation.
- Side effects (I/O, API calls) are isolated from pure calculation functions.
- API keys and secrets stay in environment variables (`.env`), never in source code.
