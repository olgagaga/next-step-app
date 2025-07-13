"""
Database connection and session management for the API.
This module handles SQLAlchemy database connections and sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Database URL - using SQLite for now
# In production, you might want to use PostgreSQL or MySQL
DB_PATH = str(Path(__file__).parent.parent / "data" / "scraper.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create the SQLAlchemy engine
# connect_args is needed for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Dependency function to get a database session.
    This is used by FastAPI to inject database sessions into endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 