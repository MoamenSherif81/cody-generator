from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel

from app.models.message import Message
from app.schemas.code import AnonymousCodeResponse


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

class SendMessageResponse(MessageResponse):
    compiled : Optional[AnonymousCodeResponse]
    @classmethod
    def from_message(cls, message: Message):
        code = None
        if message.code:
            code = AnonymousCodeResponse.from_dsl(message.code)
        return cls(
            id=message.id,
            timestamp=message.timestamp,
            content=message.content,
            code=message.code,
            compiled=code
        )

class ChatResponse(BaseModel):
    record_id: int
    messages: List[MessageResponse]


class LLmMessageFormat(BaseModel):
    role: Literal["system", "user"]
    content: str
