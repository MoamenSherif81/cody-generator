from pydantic import BaseModel, Field

from app.schemas.Situation.AiModels import AiModel
from app.schemas.Situation.SituationLanguage import Language


class GetSituation(BaseModel):
    language: Language
    aiModel: AiModel
    situationDescription: str = Field(..., description="Description with the asked language")
    dsl: str = Field(..., description="Dsl for the current situation")
    html: str = Field(..., description="Html for the Generated Dsl")
    css: str = Field(..., description="Css for the Generated Dsl")
