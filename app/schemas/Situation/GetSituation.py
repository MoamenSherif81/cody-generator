from pydantic import BaseModel, Field

from app.schemas.Situation.AiModels import AiModel
from app.schemas.Situation.SituationLanguage import Language


class GetSituation(BaseModel):
    language: Language
    aiModel: AiModel
    SituationDescription: str = Field(..., description="Description with the asked language")
    Dsl: str = Field(..., description="Dsl for the current situation")
    Html: str = Field(..., description="Html for the Generated Dsl")
    Css: str = Field(..., description="Css for the Generated Dsl")
