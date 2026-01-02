from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    model_config = {
        "env_file": "../.env",
        "extra": "ignore"
    }

settings = Settings()
