from sqlmodel import create_engine, Session, SQLModel
from .config import settings

if not settings.DATABASE_URL:
    # Fallback for development if .env is missing
    sqlite_url = "sqlite:///./database.db"
    settings.DATABASE_URL = sqlite_url

engine = create_engine(settings.DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
