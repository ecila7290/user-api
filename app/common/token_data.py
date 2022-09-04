import datetime

from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    access_token: str


class TokenData(BaseModel):
    email: EmailStr
    sub: str
    exp: datetime.datetime
