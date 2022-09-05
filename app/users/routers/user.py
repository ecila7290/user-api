from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.common.exceptions import (
    ConflictException,
    InvalidValueException,
    EntityNotFoundException,
    UnauthorizedException,
    BadRequestException,
)
from app.common.token_data import TokenResponse, TokenData
from app.common.utils.token_helper import validate_token
from app.users.entities.schemas.user import UserCreate, User, UserSignin, UserPasswordReset
from app.users.entities.schemas.verification import Verification, VerificationCreate
from app.users.repositories.user_repository import UserRepository
from app.users.repositories.verification_repository import VerificationRepository
from app.users.services.user import UserService
from app.users.services.verification import VerificationService

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
def user_signup(user: UserCreate, db: Session = Depends(get_db)):
    verification_code = user.verification_code
    del user.verification_code

    service = UserService(UserRepository(db=db), VerificationRepository(db=db))

    try:
        return service.create_user(user, verification_code)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidValueException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/verification", status_code=status.HTTP_201_CREATED, response_model=Verification)
def user_verification(verification: VerificationCreate, db: Session = Depends(get_db)):

    service = VerificationService(VerificationRepository(db=db))

    try:
        return service.create_verification(verification)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidValueException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/signin", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def user_signin(signin_info: UserSignin, db: Session = Depends(get_db)):
    """로그인 API 입니다.
    이메일, 닉네임, 핸드폰 번호 중 하나로 로그인이 가능합니다.
    """
    service = UserService(UserRepository(db=db))

    try:
        return service.signin_user(signin_info)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/mypage", response_model=User)
def user_mypage(token: TokenData = Depends(validate_token), db: Session = Depends(get_db)):
    service = UserService(UserRepository(db=db))
    try:
        return service.read_user(token)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/passwordReset")
def user_password_reset(user_info: UserPasswordReset, db: Session = Depends(get_db)):
    service = UserService(UserRepository(db=db), VerificationRepository(db=db))

    try:
        return service.reset_password(user_info)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
