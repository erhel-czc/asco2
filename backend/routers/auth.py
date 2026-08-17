import os
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlmodel import Session, select

from backend.db import get_db
from backend.models import User, UserSession
from backend.schemas import UserLogin, UserRead
from backend.security import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Keep the cookie name stable so the frontend and backend use the same session.
SESSION_COOKIE_NAME = "asco2_session"
SESSION_DURATION = timedelta(days=7)


def _cookie_secure() -> bool:
    # Only send the cookie over HTTPS in production.
    return os.getenv("ENV", "development") == "production"


def _session_expires_at() -> datetime:
    return datetime.now() + SESSION_DURATION


def _create_session(session: Session, user_id: int) -> UserSession:
    # A random token is enough here because the real state lives in the database.
    db_session = UserSession(
        token=secrets.token_urlsafe(32),
        user_id=user_id,
        expires_at=_session_expires_at(),
    )
    session.add(db_session)
    session.commit()
    session.refresh(db_session)
    return db_session


def get_current_user(request: Request, session: Session = Depends(get_db)) -> User:
    # Read the session cookie and resolve it against the database.
    token = request.cookies.get(SESSION_COOKIE_NAME)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    db_session = session.get(UserSession, token)

    if db_session is None or db_session.expires_at <= datetime.now():
        if db_session is not None:
            session.delete(db_session)
            session.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user = session.get(User, db_session.user_id)

    if user is None:
        session.delete(db_session)
        session.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return user


@router.post("/login", response_model=UserRead)
def login(payload: UserLogin, response: Response, session: Session = Depends(get_db)):
    # Normalize email so the same account can be found regardless of casing.
    email = payload.email.lower().strip()
    db_user = session.exec(select(User).where(User.email == email)).first()

    if db_user is None or not verify_password(payload.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")

    db_session = _create_session(session, db_user.id)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=db_session.token,
        httponly=True,
        secure=_cookie_secure(),
        samesite="lax",
        max_age=int(SESSION_DURATION.total_seconds()),
        path="/",
    )

    return db_user


@router.post("/logout")
def logout(request: Request, response: Response, session: Session = Depends(get_db)):
    # Remove the current session row and clear the browser cookie.
    token = request.cookies.get(SESSION_COOKIE_NAME)

    if token:
        db_session = session.get(UserSession, token)
        
        if db_session is not None:
            session.delete(db_session)
            session.commit()

    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")

    return {"message": "Logged out"}


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    # Small helper for the frontend: "who am I right now?"
    return current_user
