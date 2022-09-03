from sqlalchemy import Column, String, DateTime

from app.common.database import Base
from app.common.utils.datetime_helper import utcnow
from app.common.utils.uuid import uuid4


class Verification(Base):
    __tablename__ = "verifications"

    id = Column(String, primary_key=True, default=uuid4, index=True)
    phone = Column(String, unique=True, index=True)
    code = Column(String)
    created_at = Column(DateTime(timezone=True), default=utcnow)
