from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.common.exceptions import ConflictException, InvalidValueException
from app.users.entities.schemas.user import UserCreate, User
from app.users.entities.schemas.verification import Verification, VerificationCreate
from app.users.repositories.user_repository import UserRepository
from app.users.repositories.verification_repository import VerificationRepository
from app.users.services.user import UserService
from app.users.services.verification import VerificationService

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
    # 처리하기
    verification_code = user.verification_code
    del user.verification_code
    service = UserService(UserRepository(db=db), VerificationRepository(db=db))
    try:
        return service.create_user(user, verification_code)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidValueException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/verification", status_code=status.HTTP_201_CREATED, response_model=Verification)
async def user_verification(verification: VerificationCreate, db: Session = Depends(get_db)):
    service = VerificationService(VerificationRepository(db=db))
    try:
        return service.create_verification(verification)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidValueException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
