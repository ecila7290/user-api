import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    SQLALCHEMY_TEST_DATABASE_URL: str = "sqlite:///./test.db"
    SQLALCHEMY_DATABASE_URL: str = os.environ.get("DB_URL", "sqlite:///./user_app.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", "7c38bf24e9b734c99882c69bb1974d7d56e555250eed0e0a27c8cdec8cc92655")
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")


settings = Settings()
