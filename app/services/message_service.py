from datetime import datetime

from sqlalchemy.orm import Session

from Ai_Agents import get_agent
from Ai_Agents.models import ModelMessage, ModelResponse
from LLM.Utils import parse_json
from app.models.message import Message
from app.models.record import Record
from app.schemas.message import MessageCreate, MessageResponse, ChatResponse, SendMessageResponse


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
        message = Message(
            record_id=record_id,
            content=data.content,
            code=data.code,
            timestamp=datetime.utcnow(),
            role="user"
        )
        history = self._get_message_history(record_id, 10)
        msg = self._convert_message_to_llm_message(message)
        llm_response: ModelResponse = get_agent().chat(msg, history)
        aiResponse = Message(
            record_id=record_id,
            content=llm_response.message,
            code=llm_response.code,
            timestamp=datetime.utcnow(),
            role="system"
        )
        self.db.add(message)
        self.db.add(aiResponse)
        self.db.commit()
        self.db.refresh(message)
        self.db.refresh(aiResponse)

        return SendMessageResponse.from_message(aiResponse)

    def _convert_message_to_llm_message(self, message: Message) -> ModelMessage:
        return ModelMessage(
            role="user",
            message=message.content,
            code=message.code
        )

    def clear_chat(self, record_id: int) -> ChatResponse:
        record = self.db.query(Record).filter_by(id=record_id).first()
        if not record:
            raise Exception("Record not found")
        self.db.query(Message).filter_by(record_id=record_id).delete()
        self.db.commit()
        return ChatResponse(record_id=record.id, messages=[])

    # def _clean_response(self, res: str) -> str:
    #     try:
    #         jsn = parse_json(res)
    #         return jsn["dsl"]
    #     except:
    #         res = res.replace("`", "")
    #         res = res.replace("dsl", "")
    #         res = res.replace("\n", "")
    #         if res.startswith("{") and res.endswith("}"):
    #             res = res[1:-1]
    #         return res

    def _get_message_history(self, record_id, limit) -> list[ModelMessage]:
        """
        Returns the last `limit` messages for the given record_id,
        ordered by timestamp ascending (oldest first).
        """
        messages = (
            self.db.query(Message)
            .filter(Message.record_id == record_id)
            .order_by(Message.timestamp.asc())
            .limit(limit)
            .all()
        )
        if not messages:
            return []
        ret_messages = [
            ModelMessage(
                role=mes.role,
                message=mes.content,
                code=mes.code
            )
            for mes in messages
        ]
        return ret_messages
