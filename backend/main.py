import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.db import init_db
from backend.routers.auth import router as auth_router
from backend.routers.associations import router as associations_router
from backend.routers.public import router as public_router
from backend.routers.users import router as users_router
from backend.routers.agrybalise import router as agrybalise_router

app = FastAPI(title="AsCO2 API", version="26.8.20")

ROOT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT_DIR / "frontend"
BACKEND_DIR = ROOT_DIR / "backend"
# Directories watched in development to detect template/style/script edits.
DEV_WATCH_DIRS = (
    FRONTEND_DIR / "templates",
    FRONTEND_DIR / "style",
    FRONTEND_DIR / "js",
    BACKEND_DIR ,
)

DEV_WATCH_EXTENSIONS = {".html", ".css", ".scss", ".js", ".py"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

ENV = os.getenv("ENV", "development")


def _frontend_revision() -> int:
    # Expose a monotonic "revision" based on the newest frontend file mtime.
    # The browser polls this value and reloads when it increases.
    latest_mtime_ns = 0

    for directory in DEV_WATCH_DIRS:
        # Skip missing directories to keep development startup resilient.
        if not directory.exists():
            continue

        for file_path in directory.rglob("*"):
            # Only track relevant frontend source/assets, not every file.
            if not file_path.is_file() or file_path.suffix not in DEV_WATCH_EXTENSIONS:
                continue

            # Keep the highest mtime across watched files as the current revision.
            current_mtime_ns = file_path.stat().st_mtime_ns
            
            if current_mtime_ns > latest_mtime_ns:
                latest_mtime_ns = current_mtime_ns

    return latest_mtime_ns

if ENV == "production":
    @app.middleware("http")
    async def enforce_https(request: Request, call_next):
        """Redirect any plain-HTTP request to HTTPS in production."""
        if request.headers.get("x-forwarded-proto", "https") == "http":
            url = request.url.replace(scheme="https")
            return RedirectResponse(url, status_code=301)

        return await call_next(request)
else:
    @app.get("/__dev/revision")
    def read_frontend_revision():
        """Return the current frontend revision polled by the dev auto-reload script."""
        return {"revision": _frontend_revision()}

app.include_router(public_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(associations_router)
app.include_router(agrybalise_router)
