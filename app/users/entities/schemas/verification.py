import datetime

from pydantic import BaseModel, Field

from app.common.utils.datetime_helper import utcnow
from app.common.utils.uuid import uuid4


class VerificationBase(BaseModel):
    code: str


class VerificationCreate(VerificationBase):
    id: str = Field(default_factory=uuid4)
    code: str
    phone: str
    created_at: datetime.datetime = Field(default_factory=utcnow)

    def __setattr__(self, name: str, value: any) -> None:
        if name in {"id", "created_at"}:
            raise AttributeError(f"Cannot assign new value for {name!r}")
        super().__setattr__(name, value)
