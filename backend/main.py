from fastapi import FastAPI

from backend.db import init_db
from backend.routers.associations import router as associations_router
from backend.routers.public import router as public_router
from backend.routers.reports import router as reports_router
from backend.routers.users import router as users_router

app = FastAPI(title="AsCO2 API", version="26.7.26")

init_db()

app.include_router(public_router)
app.include_router(users_router)
app.include_router(associations_router)
app.include_router(reports_router)
