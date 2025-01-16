from sqlmodel import SQLModel, Field, Session
from typing import Optional
from database import engine
from contextlib import contextmanager
from datetime import datetime


class InfoData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    link: str
    date_added: Optional[str] = datetime.now().strftime("%Y-%m-%d")
    time: Optional[str] = datetime.now().strftime("%H:%M:%S")


class NewsData(SQLModel, table=True):
    news_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    featured_image: Optional[str] = None
    date_added: Optional[str] = datetime.now().strftime("%Y-%m-%d")
    time: Optional[str] = datetime.now().strftime("%H:%M:%S")
    
    # Foreign key to link to InfoData
    info_id: Optional[int] = Field(default=None, foreign_key="infodata.id")
    

SQLModel.metadata.create_all(engine)
                                                 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()