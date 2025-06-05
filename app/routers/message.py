from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.message import MessageCreate, MessageResponse, ChatResponse
from app.services.message_service import MessageService
from app.config.database import get_db

router = APIRouter(prefix="/records/{record_id}/chat", tags=["Chat"])

def get_message_service(db: Session = Depends(get_db)):
    return MessageService(db)

@router.get("/", response_model=ChatResponse)
def get_chat(record_id: int, service: MessageService = Depends(get_message_service)):
    try:
        return service.get_chat(record_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/message", response_model=MessageResponse)
def send_message(record_id: int, message: MessageCreate, service: MessageService = Depends(get_message_service)):
    try:
        return service.send_message(record_id, message)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/clear", response_model=ChatResponse)
def clear_chat(record_id: int, service: MessageService = Depends(get_message_service)):
    try:
        return service.clear_chat(record_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
