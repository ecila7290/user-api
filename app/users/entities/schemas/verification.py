import datetime

from pydantic import BaseModel, Field


class VerificationBase(BaseModel):
    phone: str = Field(example="+821012345678")


class VerificationCreate(VerificationBase):
    pass


class Verification(VerificationBase):
    id: str
    code: str
    created_at: datetime.datetime

    class Config:
        # Tells the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
        orm_mode = True
