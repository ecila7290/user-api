from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# #this is to include backend dir in sys.path so that we can import from db,main.py

from app.common.database import Base, get_db
from app.common.config import API_V1
from app.users.routers import user


def start_app():
    app = FastAPI()
    app.include_router(user.router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    _app = start_app()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[TestingSessionLocal, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: TestingSessionLocal) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        client.base_url += API_V1
        client.base_url = client.base_url.rstrip("/") + "/"
        yield client
