from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app.config.database import Base


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("records.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    code = Column(Text, nullable=True)
    role = Column(Text, nullable=False)
    record = relationship("Record", back_populates="messages")
