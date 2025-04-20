# News Scraper with Prefect

A robust news scraping and storage system that automatically collects articles from Citinewsroom, stores them in a PostgreSQL database, and manages the data lifecycle using **Prefect** for orchestration.

**Blog about the whole setup and process soon**


1. **Data Collection**
   - Scrapes news articles from Citinewsroom
   - Collects metadata (title, link) and detailed content
   - Handles pagination and content extraction
   - Implements error handling and retry mechanisms

2. **Data Storage**
   - Uses Neon PostgreSQL for cloud database storage
   - Implements two main tables:
     - `InfoData`: Stores article metadata
     - `NewsData`: Stores detailed article content

3. **Orchestration**
   - Prefect Cloud for workflow orchestration
   - Scheduled runs every 10 hours
   - Automatic deployment from GitHub
   - Work pool management for scalability

## Technical Decisions

### Why Neon PostgreSQL?
- Serverless PostgreSQL database
- Automatic scaling and maintenance
- Built-in connection pooling
- SSL security by default
- Free tier available for development

### Why Prefect Cloud?
- Reliable workflow orchestration
- Built-in monitoring and logging
- Easy deployment from GitHub
- Automatic retries and error handling
- Scalable worker pools

### Database Schema

```sql
-- InfoData Table
CREATE TABLE infodata (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP
);

-- NewsData Table
CREATE TABLE newsdata (
    news_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    featured_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP,
    info_id INTEGER REFERENCES infodata(id)
);
```

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/Personal-News.git
   cd Personal-News
   ```

2. **Install Dependencies**
   ```bash
   pip install -e .
   ```

3. **Database Setup**
   - Create a Neon PostgreSQL database
   - Update the connection string in `app/models.py`
   - The database tables will be created automatically on first run

4. **Prefect Setup**
   ```bash
   # Login to Prefect Cloud
   prefect cloud login

   # Create a work pool
   prefect work-pool create news-scraper-pool

   # Deploy the flow
   prefect deploy
   ```

## Configuration

### Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection string
- `PREFECT_API_URL`: Prefect Cloud API URL

### Prefect Deployment
- Schedule: Every 10 hours
- Work Pool: news-scraper-pool
- Storage: GitHub repository
- Tags: ["news", "scraping"]

## Features

1. **Automated Data Collection**
   - Scheduled scraping of news articles
   - Automatic content extraction
   - Error handling and retries

2. **Data Management**
   - Soft delete for old articles
   - Automatic cleanup of data older than 7 days
   - Data integrity through foreign key relationships

3. **Monitoring and Logging**
   - Comprehensive logging system
   - Prefect Cloud monitoring
   - Error tracking and reporting

## Development

### Local Testing
```bash
# Run the flow locally
python -m app.main

# Test database connection
python -m app.test_db
```

### Deployment
```bash
# Deploy to Prefect Cloud
prefect deploy

# Run the deployment
prefect deployment run 'scrape-and-store-articles/news-scraper'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.  

