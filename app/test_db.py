from sqlmodel import create_engine
from sqlalchemy import text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    try:
        # Direct database connection string
        DATABASE_URL = "postgresql://neondb_owner:npg_yNf6PZwCQs8W@ep-odd-butterfly-a4utxto8-pooler.us-east-1.aws.neon.tech/newsdata?sslmode=require"
        
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("\nSuccessfully connected to database!")
            print(f"Connection URL: {DATABASE_URL.replace('npg_yNf6PZwCQs8W', '********')}")
            
        return True
    except Exception as e:
        print(f"\nError connecting to database: {str(e)}")
        return False

if __name__ == "__main__":
    test_database_connection() 