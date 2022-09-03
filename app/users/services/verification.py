from app.common.exceptions import InvalidValueException
from app.common.utils.phone_helper import is_valid_phone
from app.users.repositories.verification_repository import VerificationRepository
from app.users.entities.models.verification import Verification
from app.users.entities.schemas.verification import VerificationCreate


class VerificationService:
    def __init__(self, verification_repository: VerificationRepository) -> None:
        self.verification_repository = verification_repository

    def create_verification(self, verification: VerificationCreate):
        phone_number = verification.phone
        verification.phone = phone_number.replace("-", "")
        if not is_valid_phone(verification.phone):
            raise InvalidValueException("Invalid phone number.")
        created_verification = self.verification_repository.create(Verification(**verification.dict()))
        return created_verification
