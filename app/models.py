from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Optional
from contextlib import contextmanager
from datetime import datetime
import os
import logging
from prefect_sqlalchemy import DatabaseCredentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Direct database connection string
DATABASE_URL = "postgresql://neondb_owner:npg_yNf6PZwCQs8W@ep-odd-butterfly-a4utxto8-pooler.us-east-1.aws.neon.tech/newsdata?sslmode=require"
logger.info("Using direct database connection")

# Create engine with PostgreSQL-specific settings
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  
    pool_size=5,         
    max_overflow=10      
)


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
    logger.info("Creating database and tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database and tables created successfully")


@contextmanager
def get_session():
    """Provide a transactional session."""
    logger.info("Creating new database session")
    session = Session(engine)
    try:
        yield session
        session.commit()
        logger.info("Session committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Session error: {str(e)}")
        raise
    finally:
        session.close()
        logger.info("Session closed")
