from datetime import datetime

from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.record import Record
from app.schemas.message import MessageCreate, MessageResponse, ChatResponse


class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def get_chat(self, record_id: int) -> ChatResponse:
        record = self.db.query(Record).filter_by(id=record_id).first()
        if not record:
            raise Exception("Record not found")
        return ChatResponse(
            record_id=record.id,
            messages=[MessageResponse.from_message(msg) for msg in record.messages]
        )

    def send_message(self, record_id: int, data: MessageCreate) -> MessageResponse:
        record = self.db.query(Record).filter_by(id=record_id).first()
        if not record:
            raise Exception("Record not found")
        message = Message(
            record_id=record_id,
            content=data.content,
            code=data.code,
            timestamp=datetime.utcnow()
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return MessageResponse.from_message(message)

    def clear_chat(self, record_id: int) -> ChatResponse:
        record = self.db.query(Record).filter_by(id=record_id).first()
        if not record:
            raise Exception("Record not found")
        self.db.query(Message).filter_by(record_id=record_id).delete()
        self.db.commit()
        return ChatResponse(record_id=record.id, messages=[])
