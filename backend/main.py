import os

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.db import init_db
from backend.routers.associations import router as associations_router
from backend.routers.public import router as public_router
from backend.routers.reports import router as reports_router
from backend.routers.users import router as users_router
from backend.routers.agrybalise import router as agrybalise_router

app = FastAPI(title="AsCO2 API", version="26.8.14")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

ENV = os.getenv("ENV", "development")

if ENV == "production":
    @app.middleware("http")
    async def enforce_https(request: Request, call_next):
        """Redirect any plain-HTTP request to HTTPS in production."""
        if request.headers.get("x-forwarded-proto", "https") == "http":
            url = request.url.replace(scheme="https")
            return RedirectResponse(url, status_code=301)

        return await call_next(request)

app.include_router(public_router)
app.include_router(users_router)
app.include_router(associations_router)
app.include_router(reports_router)
app.include_router(agrybalise_router)
