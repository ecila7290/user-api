import datetime
from typing import Union

from pydantic import BaseModel, EmailStr, Field

from app.common.utils.datetime_helper import utcnow
from app.common.utils.uuid import uuid4


class UserBase(BaseModel):
    phone: str
    is_active: bool


class UserCreate(UserBase):
    id: str = Field(default_factory=uuid4)
    name: str
    email: EmailStr
    nickname: str
    phone: str
    password: str
    verification_code: str
    is_active: bool = Field(default=True)
    created_at: datetime.datetime = Field(default_factory=utcnow)

    def __setattr__(self, name: str, value: any) -> None:
        if name in {"id", "created_at", "is_active"}:
            raise AttributeError(f"Cannot assign new value for {name!r}")
        super().__setattr__(name, value)


class UserUpdate(UserBase):
    phone: Union[str, None] = None
    password: Union[str, None] = None
    new_password: Union[str, None] = None
    is_active: Union[bool, None] = None
    last_updated_at: datetime.datetime = Field(default_factory=utcnow)

    def __setattr__(self, name: str, value: any) -> None:
        if name in {"id", "created_at"}:
            raise AttributeError(f"Cannot assign new value for {name!r}")
        super().__setattr__(name, value)


class User(UserBase):
    id: str
    name: str
    email: EmailStr
    nickname: str
    created_at: datetime.datetime
    last_updated_at: datetime.datetime
    last_signed_in_at: datetime.datetime

    class Config:
        # Tells the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
        orm_mode = True
