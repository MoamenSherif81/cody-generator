from pydantic import BaseModel, Field


class AskQuestion(BaseModel):
    situation: str = Field(description="Situation or description of webpage should generate it's corresponding DSL")


class AnswerQuestion(BaseModel):
    Response: str = Field(..., description="The Ai Agent Response of the request (don't contain code) just explanation")
    DslCode: str = Field(..., description="DSL Code Corresponding to the situations")
