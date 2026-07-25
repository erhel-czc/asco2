from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from backend.db import get_db
from backend.models import User
from backend.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def read_users(session: Session = Depends(get_db)):
    """Endpoint to retrieve all users."""
    users = session.exec(select(User)).all()
    return users


@router.post("", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    """Endpoint to create a new user."""
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
