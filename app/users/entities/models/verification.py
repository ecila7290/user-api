from sqlalchemy import Column, String, DateTime

from app.common.database import Base


class Verification(Base):
    __tablename__ = "verifications"

    id = Column(String, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    nickname = Column(String, unique=True, index=True)
    code = Column(String)
    created_at = Column(DateTime, timezone=True)
