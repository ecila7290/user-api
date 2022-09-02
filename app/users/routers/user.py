from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.common.exceptions import ConflictException
from app.users.entities.schemas.user import UserCreate
from app.users.repositories.user_repository import UserRepository
from app.users.services.user import UserService

router = APIRouter()


@router.post("/signup")
async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
    verification_code = user.verification_code
    del user.verification_code
    service = UserService(UserRepository(db=db))
    try:
        return service.create_user(user)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
