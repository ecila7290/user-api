from app.common.utils.password_helper import hash_password
from app.users.repositories.user_repository import UserRepository
from app.users.entities.models.user import User
from app.users.entities.schemas.user import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, user: UserCreate):
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        created_user = self.user_repository.create(User(**user.dict()))
        return created_user
