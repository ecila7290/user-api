import random

from sqlalchemy import Column, String, DateTime

from app.common.database import Base
from app.common.utils.datetime_helper import utcnow
from app.common.utils.uuid import uuid4


def generate_verification_code():
    return "".join(random.choice("0123456789") for _ in range(6))


class Verification(Base):
    __tablename__ = "verifications"

    id = Column(String, primary_key=True, default=uuid4, index=True)
    phone = Column(String, index=True)
    code = Column(String, default=generate_verification_code)
    created_at = Column(DateTime(timezone=True), default=utcnow)
