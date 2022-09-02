from pydantic import BaseModel

from app.common.repository.sqlite_repository import SqliteRepository
from app.users.entities.models.user import User
from app.users.entities.schemas.user import UserCreate, UserUpdate, UserBase

M = User


class UserRepository(SqliteRepository[M, UserCreate, UserUpdate]):
    Entity = M

    def __init__(self, db) -> None:
        super().__init__()
        self.db = db
