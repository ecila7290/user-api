from app.common.repository.sqlite_repository import SqliteRepository
from app.users.entities.models.user import User

M = User


class UserRepository(SqliteRepository[User]):
    Entity = M

    def __init__(self, db) -> None:
        super().__init__()
        self.db = db
