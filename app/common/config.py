import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    SQLALCHEMY_TEST_DATABASE_URL: str = "sqlite:///./test.db"
    SQLALCHEMY_DATABASE_URL: str = os.environ.get("DB_URL", "sqlite:///./user_app.db")


settings = Settings()
