from datetime import timedelta

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.common.config import settings
from app.common.token_data import TokenData
from app.common.utils.datetime_helper import utcnow

TOKEN_EXPIRES_IN_SEC = 60 * 60


def create_access_token(user_data: dict):
    encoded_data = user_data.copy()
    encoded_data.update({"exp": utcnow() + timedelta(seconds=TOKEN_EXPIRES_IN_SEC)})
    access_token = jwt.encode(encoded_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return access_token


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    토큰을 검증하고 TokenData 타입으로 되돌려준다.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM,
            options={"verify_signature": False, "verify_aud": False, "verify_iss": False},
        )
        return TokenData(**payload)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
