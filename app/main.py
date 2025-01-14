import requests as req
import json
from bs4 import BeautifulSoup
import logging
from models import InfoData, create_db_and_tables, get_session

url = "https://citinewsroom.com/2025/01/"
response = req.get(url)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all('div', class_='jeg_thumb')
data = []

def collect_info():
    for article in articles:
        link = article.find('a')['href']
        title_div = article.find_next('h3', class_='jeg_post_title')
        title = title_div.get_text(strip=True) if title_div else 'No title found'
        data.append({'title': title, 'link': link})

def insert_data(session, data, model):
    logging.basicConfig(level=logging.INFO)
    for info in data:
        info_data = model(title=info['title'], link=info['link'])
        session.add(info_data)
        logging.info(f"Added info: {info}")
    session.commit()
    logging.info("Data committed to the database")

if __name__ == "__main__":
    create_db_and_tables()  # Make sure to create the database tables
    collect_info()
    json_data = json.dumps(data, indent=4)
    print(json_data)
    
    with get_session() as session:
        insert_data(session, data, InfoData)
