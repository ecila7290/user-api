import datetime
from typing import Union

from pydantic import BaseModel, EmailStr, Field, PrivateAttr

from app.common.utils.datetime_helper import utcnow
from app.common.utils.uuid import uuid4


class UserBase(BaseModel):
    phone: str


class UserCreate(UserBase):
    name: str
    email: EmailStr
    nickname: str
    password: str
    verification_code: str


class UserUpdate(UserBase):
    phone: Union[str, None] = None
    password: Union[str, None] = None
    new_password: Union[str, None] = None
    is_active: Union[bool, None] = None


class User(UserBase):
    id: str
    name: str
    email: EmailStr
    nickname: str
    is_active: bool
    created_at: datetime.datetime
    last_updated_at: datetime.datetime
    last_signed_in_at: datetime.datetime

    class Config:
        # Tells the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
        orm_mode = True
