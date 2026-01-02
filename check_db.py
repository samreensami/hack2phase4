import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv

# Load root .env
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Add backend to path for imports
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from core.database import engine

def check_connection():
    print(f"Connecting to: {os.getenv('DATABASE_URL')[:30]}...")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.fetchone()[0] == 1:
                print("Database connection: LIVE")
            else:
                print("Database connection: FAILED (Unexpected result)")
    except Exception as e:
        print(f"Database connection: FAILED")
        print(f"Error: {e}")

if __name__ == "__main__":
    check_connection()
