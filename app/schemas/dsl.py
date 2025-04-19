from pydantic import BaseModel

class DSLContentRequest(BaseModel):
    dsl_content: str
