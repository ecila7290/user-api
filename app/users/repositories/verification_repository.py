from app.common.repository.sqlite_repository import SqliteRepository
from app.users.entities.models.verification import Verification

M = Verification


class VerificationRepository(SqliteRepository[Verification]):
    Entity = M

    def __init__(self, db) -> None:
        super().__init__()
        self.db = db
