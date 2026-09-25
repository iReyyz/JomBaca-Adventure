import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_default")
    
    # Supabase / PostgreSQL database connection setup
    db_url = os.getenv("DATABASE_URL")
    
    # Handle SQLAlchemy compatibility for postgres:// and postgresql:// URI prefixes
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+psycopg2://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    # Local fallback sqlite DB if DATABASE_URL is not set or empty
    SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///jombaca.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

