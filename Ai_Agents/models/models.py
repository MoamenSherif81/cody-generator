from typing import Literal, Optional

from pydantic import BaseModel


class ModelMessage(BaseModel):
    role: Literal["user", "system"]
    message: str
    code: Optional[str] = None

    def __repr__(self):
        return f"Role: {self.role}, Message = {self.message[:20]}{'...' if len(self.message) > 20 else ''}"
    def __str__(self):
        return self.__repr__()

class ModelResponse(BaseModel):
    message: Optional[str]
    code: Optional[str]
