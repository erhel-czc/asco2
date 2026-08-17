from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from fastapi import HTTPException

from backend.db import get_db
from backend.models import User
from backend.schemas import UserCreate, UserRead
from backend.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def read_users(session: Session = Depends(get_db)):
    """Endpoint to retrieve all users."""
    users = session.exec(select(User)).all()
    return users


@router.post("", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    """Receive a plaintext password, hash it securely, then persist the user."""

    # Normalize the email so sign-in uses the exact same value later.
    user.email = user.email.strip().lower()
    
    existing_user = session.exec(select(User).where(User.email == user.email)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
