from pydantic import BaseModel, Field


class Situation(BaseModel):
    SituationDescription: str = Field(description="Web page description",
                                      examples=["I wanna make login page"])


class GenerateQuestions(BaseModel):
    id: int = Field(description="Unique identifier for the question set")
    situation: Situation = Field(min_length=3, max_length=6,
                                 description="Situation should have the same output structure and matches the same generated DSL")
    DslCode: str = Field(..., description="DSL Code Corresponding to the situations")
