from pydantic import BaseModel, Field

from app.schemas.Situation.AiModels import AiModel
from app.schemas.Situation.SituationLanguage import Language


class AcceptSituation(BaseModel):
    userName: str = Field(..., description="Name of the user ")
    language: Language
    aiModel: AiModel
    situationDescription: str = Field(..., description="Description with the asked language")
    dsl: str = Field(..., description="Dsl for the current situation")

    @staticmethod
    def get_AcceptSituation_description() -> str:
        languages = "\n".join([f"- **{lang.value}**" for lang in Language])
        ai_models = "\n".join([f"- **{model.value}**" for model in AiModel])
        return (
            "## Accept Situation\n\n"
            "**Available Options:**\n\n"
            f"**Languages:**\n{languages}\n\n"
            f"**AI Models:**\n{ai_models}\n\n"
            "**Notes:**\n"
            "- The `language` and `aiModel` fields must match one of the listed options.\n"
        )
