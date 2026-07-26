from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from backend.db import get_db
from backend.models import Food, Stuff, Transport, Digital

router = APIRouter()


@router.get("/")
def read_root():
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