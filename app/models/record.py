from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.message import Message


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    screenshot_path = Column(String, nullable=True)
    dsl_content = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="records")
    project = relationship("Project", back_populates="records")
    messages = relationship("Message", back_populates="record", cascade="all, delete-orphan",
                            order_by=lambda: Message.timestamp)
