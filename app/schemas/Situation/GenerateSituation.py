from pydantic import BaseModel, Field

from AiModels import AiModel
from SituationLanguage import Language


class GenerateSituation(BaseModel):
    language: Language = Field(Language.Egyptian, description="Language of the target situation")
    Issuer: str = Field(..., description="the name of the user asked for the situation")
    model: AiModel = Field(AiModel.GeminiFlush2_0, description="select model to generate the situation")
