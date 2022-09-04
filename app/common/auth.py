from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from app.common.config import settings


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM,
            options={"verify_signature": False, "verify_aud": False, "verify_iss": False},
        )
        print("payload => ", payload)
    except JWTError as e:  # catches any exception
        raise HTTPException(status_code=401, detail=str(e))
