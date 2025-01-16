import requests as req
from bs4 import BeautifulSoup
import logging
from models import InfoData, NewsData, create_db_and_tables, get_session
from prefect import task, flow


url_base = "https://citinewsroom.com/2025/01/page/"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@task
def collect_info(page: int):
    """Collect article metadata (title and link) from a given page."""
    url = f"{url_base}{page}/"
    response = req.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = soup.find_all('div', class_='jeg_thumb')
    data = []

    for article in articles:
        link = article.find('a')['href']
        title_div = article.find_next('h3', class_='jeg_post_title')
        title = title_div.get_text(strip=True) if title_div else 'No title found'
        data.append({'title': title, 'link': link})
    
    return data


@task
def get_content(url: str):
    """Scrape article content and featured image from a given URL."""
    response = req.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    featured_image_div = soup.find('div', class_='jeg_featured featured_image')
    featured_image = None
    if featured_image_div:
        a_tag = featured_image_div.find('a')
        featured_image = a_tag['href'] if a_tag else None

    content_div = soup.find('div', class_='content-inner')
    if not content_div:
        return None  
    
    paragraphs = content_div.find_all('p')
    article_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

    return {
        "article_content": article_content,
        "featured_image": featured_image
    }


@task
def insert_data(session, data):
    """Insert metadata into InfoData and scrape detailed content for NewsData."""
    logging.info(f"Inserting {len(data)} articles into the database.")
    for info in data:
        # Insert metadata into InfoData
        info_record = InfoData(title=info['title'], link=info['link'])
        session.add(info_record)
        session.commit()  
        logging.info(f"Added metadata: {info}")

        # Scrape content using the link and insert into NewsData
        scraped_data = get_content(info['link'])
        if scraped_data:
            news_record = NewsData(
                title=info['title'],
                content=scraped_data["article_content"],
                featured_image=scraped_data["featured_image"]
            )
            session.add(news_record)
            logging.info(f"Added detailed content for: {info['title']}")
        else:
            logging.warning(f"Content not found for link: {info['link']}")
    
    session.commit()
    logging.info("All data committed to the database.")


@task
def scrape_and_store_articles():
    """Fetch links from the database, scrape content for each link, and insert them."""
    logging.info("Starting the scraping and storing process.")
    create_db_and_tables()  
    
    page = 1
    while True:
        data = collect_info(page)  
        
        if not data:
            logging.info("No more articles found. Ending the scraping process.")
            break
        
        with get_session() as session:
            insert_data(session, data)  
        
        page += 1  
    logging.info("Scraping and storing process completed.")

@flow
def main_flow():
    scrape_and_store_articles()

if __name__== "__main__":
    main_flow()