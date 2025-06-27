from typing import Literal, List

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "model"] = Field(...,
                                            description="Indicates whether the sender is the 'user' or 'system'.")
    content: str = Field(...,
                         description="The content of the message. If the sender is the user, this contains the user's question or input. If the sender is the system, this contains the system's response to the user.")
    code: str = Field(...,
                      description="If the sender is 'user', this contains the code or query sent to the system. If the sender is 'system', this contains the system's reply to the user's input or query.")


class ConversationStage(BaseModel):
    user_message: Message = Field(..., description="The initial prompt or follow-up question from the user.")
    system_response: Message = Field(..., description="The system's response to the user's question or prompt.")


class ChatConversation(BaseModel):
    conversation_id: int = Field(..., description="Unique identifier for the conversation.")
    language: Literal["ar", "en"] = Field(...,
                                          description="The language of the conversation. Can be either 'ar' (Arabic) or 'en' (English).")
    conversation_history: List[ConversationStage] = Field(...,
                                                          description="The history of interactions between the user and the system, including both the user's queries and the system's responses.",
                                                          min_length=4, max_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 1,
                "language": "en",
                "conversation_history": [
                    {
                        "user_message": {
                            "role": "user",
                            "content": "How do I create a login page?",
                            "code": "create login page"
                        },
                        "system_response": {
                            "role": "system",
                            "content": "To create a login page, you need to start by setting up HTML and CSS for the form.",
                            "code": "html, css setup"
                        }
                    },
                    {
                        "user_message": {
                            "role": "user",
                            "content": "Can I add a 'remember me' checkbox?",
                            "code": "add remember me checkbox"
                        },
                        "system_response": {
                            "role": "system",
                            "content": "Yes, you can add a checkbox below the password input field with an appropriate label.",
                            "code": "checkbox, html"
                        }
                    }
                ]
            }
        }
