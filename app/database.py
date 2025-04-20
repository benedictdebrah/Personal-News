from sqlmodel import create_engine, SQLModel
from app.models import InfoData, NewsData, create_db_and_tables, get_session, DATABASE_URL, engine

# No need to create a new engine, we'll use the one from models.py
SQLModel.metadata.create_all(engine)

with get_session() as session:
    # database operations
    pass
