from datetime import timedelta
from typing import List

from app.common.exceptions import InvalidValueException, EntityNotFoundException, UnauthorizedException, BadRequestException
from app.common.token_data import TokenResponse, TokenData
from app.common.utils.password_helper import hash_password, verify_password
from app.common.utils.datetime_helper import utcnow
from app.common.utils.token_helper import create_access_token
from app.users.entities.models.user import User
from app.users.entities.models.verification import Verification
from app.users.entities.schemas.user import UserCreate, UserSignin, UserPasswordReset
from app.users.entities.schemas.verification import RequestPath, Verification
from app.users.repositories.user_repository import UserRepository
from app.users.repositories.verification_repository import VerificationRepository

THREE_MINUTES_IN_SEC = 60 * 3


class UserService:
    def __init__(self, user_repository: UserRepository, verification_repository: VerificationRepository = None) -> None:
        self.user_repository = user_repository
        self.verification_repository = verification_repository

    def create_user(self, user: UserCreate, verification_code: str):
        code_in_db = self.verification_repository.query(
            limit=1, filters={"phone": user.phone, "request_path": RequestPath.SIGNUP}, sort=["-created_at"]
        )

        validate_code(code_in_db, verification_code)

        hashed_password = hash_password(user.password)
        user.password = hashed_password
        created_user = self.user_repository.create(User(**user.dict()))
        return created_user

    def signin_user(self, signin_info: UserSignin):
        password = signin_info.password
        user = self.user_repository.query(
            limit=1,
            filters={"email": signin_info.signin_id, "phone": signin_info.signin_id, "nickname": signin_info.signin_id},
            is_or=True,
        )

        if not (user and verify_password(password, user[0].password)):
            raise UnauthorizedException("Incorrect id or password")
        user = user[0]
        access_token = create_access_token({"email": user.email, "sub": user.id})

        user.last_signed_in_at = utcnow()
        self.user_repository.update(user.id, user)
        return TokenResponse(access_token=access_token)

    def read_user(self, token: TokenData):
        try:
            user = self.user_repository.read(id=token.sub)
        except EntityNotFoundException as e:
            raise e
        return user

    def reset_password(self, user_info: UserPasswordReset):
        code_in_db = self.verification_repository.query(
            limit=1, filters={"phone": user_info.phone, "request_path": RequestPath.PASSWORD_RESET}, sort=["-created_at"]
        )

        validate_code(code_in_db, user_info.verification_code)

        _filter = {"phone": user_info.phone}
        user = self.user_repository.query(limit=1, filters=_filter)

        if not (user and verify_password(user_info.current_password, user[0].password)):
            raise UnauthorizedException("Incorrect id or password")
        user = user[0]

        new_hashed_password = hash_password(user_info.new_password)
        user.password = new_hashed_password
        user.last_updated_at = utcnow()
        self.user_repository.update(user.id, user)

        return {}


def validate_code(verification: List[Verification], input: str):
    if not verification:
        raise EntityNotFoundException(id=None, entity_type=Verification)
    if input != verification[0].code:
        raise InvalidValueException(f"Incorrect verification code: {input}")
    elif (utcnow() - verification[0].created_at) > timedelta(seconds=THREE_MINUTES_IN_SEC):
        raise InvalidValueException(f"Code Expired")
