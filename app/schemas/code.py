from pydantic import BaseModel


class CodeResponse(BaseModel):
    dsl: str
    html: str
    css: str
