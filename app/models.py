from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Optional
from contextlib import contextmanager
from datetime import datetime
import os

# Get the absolute path to the app directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Create a data directory if it doesn't exist
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
# Use absolute path for database
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'news.db')}"
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
