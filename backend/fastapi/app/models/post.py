from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from ..db.postgres import Base
import uuid


class Post(Base):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_draft = Column(Boolean, default=False)
    url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(UUID(as_uuid=True), nullable=False)
    is_active = Column(Boolean, default=True)
