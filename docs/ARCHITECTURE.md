# Architecture

## Overview

AsCO₂ is a carbon-footprint web application for French associations.  
It follows a classic client/server split: a **FastAPI backend** exposes a REST API backed by SQLite, and a **vanilla HTML/CSS/JS frontend** consumes it.

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
├── frontend/              # Vanilla HTML/CSS/JS
│   ├── index.html         # Home page
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
- **Data models:** `User`, `Association`, `AssociationMembership`, `Report`, `Food`, `Transport`, `Stuff`, `Digital`.
- **Emission factors:** Agribalyse 3.1 CSV loaded locally in `backend/data/`. The `/agrybalise` router exposes search and lookup endpoints over it.
- **API docs:** available at `/docs` (Swagger UI) when the server is running.

### Adding a new page's backend logic
1. Create `backend/routers/<feature>.py` with an `APIRouter`.
2. Add schemas to `backend/schemas.py` if needed.
3. Register the router in `backend/main.py` with `app.include_router(...)`.

---

## Frontend

- **Stack:** vanilla HTML, SCSS (compiled to CSS), vanilla JS — no framework.
- **Shared components:** navbar (with burger menu) and footer are duplicated across pages but share `_navbar.scss`, `_footer.scss`, and `js/navbar.js`.
- **SCSS partials:** `_variables.scss`, `_base.scss`, `_navbar.scss`, and `_footer.scss` are shared. Each page gets its own partial (e.g., `_home.scss`) imported in `style.scss`.

### Adding a new page
1. Create `frontend/<page>.html` — copy the navbar/footer markup from `index.html`.
2. Create `frontend/style/_<page>.scss` for page-specific styles; add `@import "<page>"` in `style.scss`.
3. Create `frontend/js/<page>.js` for page-specific scripts if needed.
4. Include `<script src="./js/navbar.js" defer>` in every page.

---

## Key Conventions

- All emission factor constants must be traceable to their source (ADEME/Agribalyse).
- Units must be normalized before any calculation.
- Side effects (I/O, API calls) are isolated from pure calculation functions.
- API keys and secrets stay in environment variables (`.env`), never in source code.

