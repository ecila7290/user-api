import enum
import datetime

from pydantic import BaseModel, Field


class RequestPath(str, enum.Enum):
    SIGNUP = "signup"
    PASSWORD_RESET = "passwordReset"


class VerificationBase(BaseModel):
    phone: str = Field(example="+821012345678")


class VerificationCreate(VerificationBase):
    request_path: RequestPath

    class Config:
        use_enum_values = True


class Verification(VerificationBase):
    id: str
    code: str
    created_at: datetime.datetime

    class Config:
        # Tells the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
        orm_mode = True
        use_enum_values = True
