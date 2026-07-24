"""Database session management using SQLModel and SQLAlchemy."""

from sqlalchemy.pool import NullPool
from sqlmodel import Session, create_engine

from setting import settings

ENGINE = create_engine(settings.DB_URL, echo=True, poolclass=NullPool)


def get_db():
    """Provide a database session."""

    with Session(bind=ENGINE) as db:
        yield db
