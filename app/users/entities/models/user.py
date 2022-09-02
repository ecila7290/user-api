from sqlalchemy import Boolean, Column, String, DateTime

from app.common.database import Base
from app.common.utils.datetime_helper import utcnow
from app.common.utils.uuid import uuid4


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=uuid4(), index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    nickname = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    last_updated_at = Column(DateTime(timezone=True), nullable=True)
    last_signed_in_at = Column(DateTime(timezone=True), nullable=True)
