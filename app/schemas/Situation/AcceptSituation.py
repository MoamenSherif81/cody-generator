
from pydantic import BaseModel, Field

from app.schemas.Situation.AiModels import AiModel
from app.schemas.Situation.SituationLanguage import Language


class AcceptSituation(BaseModel):
    Issuer : str =Field(...,description="Name of the user ")
    language: Language
    aiModel: AiModel
    SituationDescription: str = Field(..., description="Description with the asked language")
    Dsl: str = Field(..., description="Dsl for the current situation")
