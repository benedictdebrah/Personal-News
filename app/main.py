import requests as req
from bs4 import BeautifulSoup
import logging
from logging.handlers import RotatingFileHandler
from app.models import InfoData, NewsData, create_db_and_tables, get_session
from prefect import task, flow
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import calendar

def get_current_month_url() -> str:
    """Get the URL for the current month's news archive."""
    current_date = datetime.utcnow()
    year = current_date.year
    month = current_date.month
    month_name = calendar.month_name[month].lower()
    return f"https://citinewsroom.com/{year}/{month:02d}/"

# Configure logging with rotating file handler
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('news_scraper.log', maxBytes=5*1024*1024, backupCount=3)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    handlers=[log_handler, logging.StreamHandler()]
)

@task
def collect_info(page: int) -> List[Dict]:
    """Collect article metadata (title and link) from a given page."""
    try:
        url_base = get_current_month_url()
        url = f"{url_base}page/{page}/"
        response = req.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        articles = soup.find_all('div', class_='jeg_thumb')
        data = []

        for article in articles:
            try:
                link = article.find('a')['href']
                title_div = article.find_next('h3', class_='jeg_post_title')
                title = title_div.get_text(strip=True) if title_div else 'No title found'
                data.append({'title': title, 'link': link})
            except Exception as e:
                logging.error(f"Error processing article: {str(e)}")
                continue
        
        return data
    except Exception as e:
        logging.error(f"Error collecting info from page {page}: {str(e)}")
        return []

@task
def get_content(url: str) -> Optional[Dict]:
    """Scrape article content and featured image from a given URL."""
    try:
        response = req.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        featured_image_div = soup.find('div', class_='jeg_featured featured_image')
        featured_image = featured_image_div.find('a')['href'] if featured_image_div else None
        
        content_div = soup.find('div', class_='content-inner')
        if not content_div:
            logging.warning(f"No content found for {url}")
            return None  
        
        paragraphs = content_div.find_all('p')
        article_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

        return {"article_content": article_content, "featured_image": featured_image}
    except Exception as e:
        logging.error(f"Error getting content from {url}: {str(e)}")
        return None

@task
def insert_data(data: List[Dict]) -> None:
    """Insert metadata into InfoData and scrape detailed content for NewsData."""
    try:
        with get_session() as session:
            logging.info(f"Inserting {len(data)} articles into the database.")
            for info in data:
                existing = session.query(InfoData).filter(
                    InfoData.link == info['link'],
                    InfoData.is_deleted == False
                ).first()
                
                if existing:
                    logging.info(f"Article already exists: {info['title']}")
                    continue
                
                info_record = InfoData(title=info['title'], link=info['link'])
                session.add(info_record)
                session.commit()
                
                scraped_data = get_content(info['link'])
                if scraped_data:
                    news_record = NewsData(
                        title=info['title'],
                        content=scraped_data["article_content"],
                        featured_image=scraped_data["featured_image"],
                        info_id=info_record.id
                    )
                    session.add(news_record)
                    logging.info(f"Added detailed content for: {info['title']}")
                else:
                    logging.warning(f"Content not found for link: {info['link']}")
                session.commit()
    except Exception as e:
        logging.error(f"Error inserting data: {str(e)}")
        raise

@task
def cleanup_old_data() -> None:
    """Delete articles older than 1 week."""
    try:
        with get_session() as session:
            one_week_ago = datetime.utcnow() - timedelta(days=7)
            old_articles = session.query(InfoData).filter(
                InfoData.created_at < one_week_ago,
                InfoData.is_deleted == False
            ).all()
            
            for article in old_articles:
                article.is_deleted = True
                article.deleted_at = datetime.utcnow()
                logging.info(f"Marked article for deletion: {article.title}")
            
            session.commit()
            logging.info(f"Cleanup completed. {len(old_articles)} articles marked for deletion.")
    except Exception as e:
        logging.error(f"Error during cleanup: {str(e)}")
        raise

@flow
def scrape_and_store_articles() -> None:
    """Fetch links, scrape content, and insert them into the database."""
    create_db_and_tables()  
    cleanup_old_data()
    
    page = 1
    total_articles = 0
    max_articles = 100  
    
    while total_articles < max_articles:
        data = collect_info(page)  
        if not data:
            break
        remaining_slots = max_articles - total_articles
        data = data[:remaining_slots] if len(data) > remaining_slots else data
        insert_data(data)
        total_articles += len(data)
        page += 1  
    
    logging.info(f"Scraping completed. Total articles: {total_articles}")

if __name__ == "__main__":
    logging.info("Starting news scraper...")
    scrape_and_store_articles()
