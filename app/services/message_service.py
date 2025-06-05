import json
from datetime import datetime

from sqlalchemy.orm import Session

from LLM.Utils import parse_json
from app.models.message import Message
from app.models.record import Record
from app.schemas.message import MessageCreate, MessageResponse, ChatResponse, SendMessageResponse
from app.services.KaggleService import LLMService


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

    def send_message(self, record_id: int, data: MessageCreate) -> SendMessageResponse:
        record = self.db.query(Record).filter_by(id=record_id).first()
        if not record:
            raise Exception("Record not found")
        llm_service = LLMService()
        message = Message(
            record_id=record_id,
            content=data.content,
            code=data.code,
            timestamp=datetime.utcnow()
        )
        llm_response =llm_service.GenerateResponse(message.to_llm_message())["response"]
        dsl= self._clean_response(llm_response)
        aiResponse = Message(
            record_id=record_id,
            content="",
            code=dsl,
            timestamp=datetime.utcnow()
        )
        self.db.add(message)
        self.db.add(aiResponse)
        self.db.commit()
        self.db.refresh(message)
        self.db.refresh(aiResponse)

        return SendMessageResponse.from_message(aiResponse)

    def clear_chat(self, record_id: int) -> ChatResponse:
        record = self.db.query(Record).filter_by(id=record_id).first()
        if not record:
            raise Exception("Record not found")
        self.db.query(Message).filter_by(record_id=record_id).delete()
        self.db.commit()
        return ChatResponse(record_id=record.id, messages=[])
    def _clean_response(self,res:str)->str:
        jsn  = parse_json(res)
        return jsn["dsl"]
    def _get_message_history(self):
        """

        """
