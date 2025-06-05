from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.models.message import Message


class MessageCreate(BaseModel):
    content: str
    code: Optional[str] = None


class MessageResponse(BaseModel):
    id: int
    timestamp: datetime
    content: str
    code: Optional[str]

    @classmethod
    def from_message(cls, message: Message):
        return cls(
            id=message.id,
            timestamp=message.timestamp,
            content=message.content,
            code=message.code
        )


class ChatResponse(BaseModel):
    record_id: int
    messages: List[MessageResponse]
