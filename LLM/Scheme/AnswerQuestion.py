from pydantic import BaseModel, Field



class AskQuestion(BaseModel):
    situation: str = Field(description="Situation or description of webpage should generate it's corresponding DSL")

class AnswerQuestion(BaseModel):
    DslCode: str = Field(..., description="DSL Code Corresponding to the situations")
