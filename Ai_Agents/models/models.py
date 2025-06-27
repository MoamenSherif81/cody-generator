from typing import Literal, Optional

from pydantic import BaseModel


class ModelMessage(BaseModel):
    role: Literal["user", "system"]
    message: str
    code: Optional[str] = None


class ModelResponse(BaseModel):
    message: Optional[str]
    code: Optional[str]
