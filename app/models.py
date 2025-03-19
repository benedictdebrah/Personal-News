from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Optional
from contextlib import contextmanager
from datetime import datetime
import os

# Load database URL from environment variable (default to SQLite if not set)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
engine = create_engine(DATABASE_URL, echo=True)


class InfoData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    link: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = None


class NewsData(SQLModel, table=True):
    news_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    featured_image: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = None

    # Foreign key linking to InfoData
    info_id: Optional[int] = Field(default=None, foreign_key="infodata.id")


def create_db_and_tables():
    """Initialize database and create tables."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    """Provide a transactional session."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
