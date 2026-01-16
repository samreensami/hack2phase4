from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    OPENAI_API_KEY: Optional[str] = None

    model_config = {
        "env_file": [".env", "backend/.env", "../.env"],
        "extra": "ignore"
    }

settings = Settings()
