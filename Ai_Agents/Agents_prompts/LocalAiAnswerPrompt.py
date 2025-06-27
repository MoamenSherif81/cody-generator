import json

from LLM.Scheme.AnswerQuestion import AnswerQuestion, AskQuestion
from app.schemas.message import LLmMessageFormat

_dsl_rules = "LLM/Examples/dsl-web.json"


def local_ai_answer_prompt(prom: str):
    with open(_dsl_rules, 'r') as file:
        dsl_rules = file.read()

    PromptMessage = [
        LLmMessageFormat(
            role="system",
            content=(
                "You are a professional Frontend Developer that can generate webpage using our own custom DSL.\n"
                "Generate the dsl for the provided situation"
                f"Dsl Rules = {dsl_rules}\n"
                f"You have to Generate response JSON {json.dumps(AnswerQuestion.model_json_schema(), ensure_ascii=False)} according the Pydantic details.\n"
                "Use only Dsl Tokens.\n"
                "Do not generate any introduction or conclusion."
                "Use a simple, visually appealing random color scheme, ensuring all selected colors belong to it."
                "don't give color to text or title token"
                "Be Creative"
            ))
        ,
        LLmMessageFormat(
            role="user",
            content=(
                "## Pydantic Details:\n"
                f"{json.dumps(AskQuestion.model_json_schema(), ensure_ascii=False)}\n\n"
                f"## Question :\n {prom} \n"
                "```json"
            )
        )

    ]
    return PromptMessage
