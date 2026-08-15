import os
from collections.abc import Generator
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

_DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "asco2.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_DEFAULT_DB_PATH}")
engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    """Create database tables if they do not exist yet."""
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for request handlers."""
    with Session(engine) as session:
        yield session
