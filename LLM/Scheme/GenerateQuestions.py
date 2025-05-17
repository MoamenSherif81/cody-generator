from typing import List
from pydantic import BaseModel, Field, Literal, constr


class Situation(BaseModel):
    SituationInArabic: str = Field(description="Web page description in Arabic", examples=["اعملى صفجة تسجيل دخول "])
    SituationInEgyptianArabic: str = Field(description="Web page description in Egyptian arabic slang",
                                           examples=["اعملى صغحة تسجيل دخول "])
    SituationInEnglish: str = Field(description="Web page description in English", examples=["I wanna make login page"])
    SituationInArabicAndEnglish: str = Field(description="Web page description that contains mix of arabic and english",
                                             examples=["اصنع لى login page", "عايز اعمل form فيها select-box"])


class GenerateQuestions(BaseModel):
    id: constr(strict=True, min_length=1) = Field(description="Unique identifier for the question set")
    Situations: List[Situation] = Field(
        min_length=3, max_length=6,
        description="Situations should have the same output structure"
    )
    DslCode: str = Field(..., description="DSL Code Corresponding to the situations")
    complexity: Literal[1, 2, 3, 4, 5] = Field(..., description="How complex the situation is. Values: 1 to 5")

