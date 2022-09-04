from datetime import timedelta

from app.common.exceptions import InvalidValueException, EntityNotFoundException
from app.common.utils.password_helper import hash_password
from app.common.utils.datetime_helper import utcnow
from app.users.repositories.user_repository import UserRepository
from app.users.repositories.verification_repository import VerificationRepository
from app.users.entities.models.user import User
from app.users.entities.models.verification import Verification
from app.users.entities.schemas.user import UserCreate
from app.users.entities.schemas.verification import RequestPath, Verification

THREE_MINUTES_IN_SEC = 60 * 3


class UserService:
    def __init__(self, user_repository: UserRepository, verification_repository: VerificationRepository) -> None:
        self.user_repository = user_repository
        self.verification_repository = verification_repository

    def create_user(self, user: UserCreate, verification_code: str):
        code_in_db = self.verification_repository.query(
            limit=1, filters={"phone": user.phone, "request_path": RequestPath.SIGNUP}, sort=["-created_at"]
        )
        if not code_in_db:
            raise EntityNotFoundException(id=None, entity_type=Verification)

        validate_code(code_in_db[0], verification_code)

        hashed_password = hash_password(user.password)
        user.password = hashed_password
        created_user = self.user_repository.create(User(**user.dict()))
        return created_user


def validate_code(verification: Verification, input: str):
    if input != verification.code:
        raise InvalidValueException(f"Incorrect verification code: {input}")
    elif (utcnow() - verification.created_at) > timedelta(seconds=THREE_MINUTES_IN_SEC):
        raise InvalidValueException(f"Code Expired")
