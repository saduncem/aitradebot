"""Database configuration using SQLAlchemy.

This module sets up a SQLite database connection using SQLAlchemy's
``create_engine`` and defines a session factory and declarative base.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# For local development we use SQLite. Replace this with your preferred
# database URL in production environments (e.g., PostgreSQL).
DATABASE_URL = "sqlite:///./trade.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
