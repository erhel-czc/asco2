from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./asco2.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    """Create database tables if they do not exist yet."""
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for request handlers."""
    with Session(engine) as session:
        yield session
