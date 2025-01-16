from fastapi import FastAPI, HTTPException, Query
from typing import List
from sqlmodel import  select
from models import NewsData, create_db_and_tables, get_session

app = FastAPI(title="News API", 
              description="API to fetch news articles from the database.",
              tags = ["News API"],
              version="0.1",
              )

@app.on_event("startup")
def on_startup():
    """Ensure the database and tables are created on startup."""
    create_db_and_tables()

@app.get("/news/", response_model=List[NewsData])
def get_all_news(skip: int = 0, limit: int = 10):
    """
    Retrieve all news articles with pagination.
    - `skip`: Number of records to skip (default 0).
    - `limit`: Maximum number of records to return (default 10).
    """
    with get_session() as session:
        news_query = select(NewsData).offset(skip).limit(limit)
        news = session.exec(news_query).all()
        if not news:
            raise HTTPException(status_code=404, detail="No news articles found.")
        return news

@app.get("/news/{news_id}", response_model=NewsData)
def get_news_by_id(news_id: int):
    """
    Retrieve a specific news article by its ID.
    - `news_id`: The ID of the news article to fetch.
    """
    with get_session() as session:
        news = session.get(NewsData, news_id)
        if not news:
            raise HTTPException(status_code=404, detail=f"News article with ID {news_id} not found.")
        return news

@app.get("/news/search/", response_model=List[NewsData])
def search_news(
    query: str = Query(..., description="Search query string."),
    skip: int = 0,
    limit: int = 10
):
    """
    Search news articles by title.
    - `query`: The search term to look for in article titles.
    - `skip`: Number of records to skip (default 0).
    - `limit`: Maximum number of records to return (default 10).
    """
    with get_session() as session:
        news_query = select(NewsData).where(NewsData.title.ilike(f"%{query}%")).offset(skip).limit(limit)
        news = session.exec(news_query).all()
        if not news:
            raise HTTPException(status_code=404, detail=f"No news articles found for query '{query}'.")
        return news
