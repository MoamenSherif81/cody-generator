from pydantic import BaseModel, Field

from app.schemas.Situation.AiModels import AiModel
from app.schemas.Situation.SituationLanguage import Language


class GenerateSituation(BaseModel):
    userName: str = Field(..., description="the name of the user asked for the situation")
    language: Language = Field(Language.Egyptian, description="Language of the target situation")
    model: AiModel = Field(AiModel.GeminiFlush2_0, description="select model to generate the situation")

    @staticmethod
    def get_GenerateSituation_description() -> str:
        languages = "\n".join([f"- **{lang.value}**" for lang in Language])
        ai_models = "\n".join([f"- **{model.value}**" for model in AiModel])
        return (
            "## Generate a New Situation\n\n"
            "Creates a new situation based on the provided language and AI model.\n\n"
            "**Available Options:**\n\n"
            f"**Languages:**\n{languages}\n\n"
            f"**AI Models:**\n{ai_models}\n\n"
            "**Notes:**\n"
            "- The `language` and `aiModel` fields must match one of the listed options.\n"
            "- The response includes generated DSL, HTML, and CSS tailored to the specified situation."
        )
