import datetime
from typing import Union

from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    phone: str = Field(example="+821012345678")


class UserCreate(UserBase):
    name: str
    email: EmailStr
    nickname: str
    password: str
    verification_code: str

    @validator("nickname")
    def nickname_alphanumeric(cls, v):
        assert v.isalnum()
        return v


class UserUpdate(UserBase):
    name: Union[str, None] = None
    phone: Union[str, None] = None
    email: Union[EmailStr, None] = None
    nickname: Union[str, None] = None
    is_active: Union[bool, None] = None


class User(UserBase):
    id: str
    name: str
    email: EmailStr
    nickname: str
    is_active: bool
    created_at: datetime.datetime
    last_updated_at: Union[datetime.datetime, None]
    last_signed_in_at: Union[datetime.datetime, None]

    class Config:
        # Tells the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
        orm_mode = True


class UserSignin(BaseModel):
    signin_id: Union[EmailStr, str] = Field(example="+821012345678 OR user@example.com OR somenickname12")
    password: str


class UserPasswordReset(BaseModel):
    current_password: str
    new_password: str
    phone: str
    verification_code: str
