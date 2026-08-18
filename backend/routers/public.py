import os
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from backend.db import get_db
from backend.models import Food, Stuff, Transport, Digital

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[2] / "frontend" / "templates")
)
# Template global used by base.html to enable/disable dev auto-refresh script.
templates.env.globals["dev_auto_reload"] = os.getenv("ENV", "development") != "production"


@router.get("/")
def read_home(request: Request):
    """Render the homepage."""
    return templates.TemplateResponse(
        request, "index.html", {"active_page": "home", "page_title": "AsCO₂"}
    )


@router.get("/login")
def read_login(request: Request):
    """Render the login page."""
    return templates.TemplateResponse(
        request,
        "login.html",
        {"active_page": "login", "page_title": "Connexion - AsCO₂"},
    )


@router.get("/signup")
def read_signup(request: Request):
    """Render the signup page."""
    return templates.TemplateResponse(
        request,
        "signup.html",
        {"active_page": "signup", "page_title": "Créer un compte - AsCO₂"},
    )

@router.get("/dashboard")
def read_dashboard(request: Request):
    """Render the dashboard page."""
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"active_page": "dashboard", "page_title": "Tableau de bord - AsCO₂"},
    )

@router.get("/methodologie")
def read_methodologie(request: Request):
    """Render the methodology page."""
    return templates.TemplateResponse(
        request,
        "methodologie.html",
        {"active_page": "methodologie", "page_title": "Méthodologie - AsCO₂"},
    )


@router.get("/api")
def read_api_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the AsCO2 API!"}


@router.get("/food")
def read_food(session: Session = Depends(get_db)):
    """Endpoint to retrieve all food entries."""
    food_entries = session.exec(select(Food)).all()
    return food_entries


@router.get("/transport")
def read_transport(session: Session = Depends(get_db)):
    """Endpoint to retrieve all transport entries."""
    transport_entries = session.exec(select(Transport)).all()
    return transport_entries


@router.get("/stuff")
def read_stuff(session: Session = Depends(get_db)):
    """Endpoint to retrieve all stuff entries."""
    stuff_entries = session.exec(select(Stuff)).all()
    return stuff_entries

@router.get("/digital")
def read_digital(session: Session = Depends(get_db)):
    """Endpoint to retrieve all digital entries."""
    digital_entries = session.exec(select(Digital)).all()
    return digital_entries