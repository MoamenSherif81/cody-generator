from pydantic import BaseModel, Field


class Situation(BaseModel):
    SituationInArabic: str = Field(description="Web page description in Arabic", examples=["اعملى صفجة تسجيل دخول "])
    SituationInEgyptianArabic: str = Field(description="Web page description in Egyptian arabic slang",
                                           examples=["اعملى صغحة تسجيل دخول "])
    SituationInEnglish: str = Field(description="Web page description in English", examples=["I wanna make login page"])
    SituationInArabicAndEnglish: str = Field(description="Web page description that contains mix of arabic and english",
                                             examples=["اصنع لى login page", "عايز اعمل form فيها select-box"])


class GenerateQuestions(BaseModel):
    id: int = Field(description="Unique identifier for the question set")
    situation: Situation = Field(min_length=3, max_length=6,
                                 description="Situation should have the same output structure and matches the same generated DSL")
    DslCode: str = Field(..., description="DSL Code Corresponding to the situations")
