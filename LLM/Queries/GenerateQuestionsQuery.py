import json

from ..Scheme.GenerateQuestions import GenerateQuestions


def GenerateMessage(DslRules):
    return [
        {
            "role": "system",
            "content": (
                "You are a Frontend Developer you want to create web page by generating website using our own custom DSL.\n"
                f"Dsl Rules = {DslRules}\n"
                "You have to Generate Situation JSON details according the Pydantic details.\n"
                "Use only Dsl Tokens.\n",
                "Generate Random Situation\n",
                "Do not generate any introduction or conclusion.",
                "Be Creative on the situation",
                "Add a bit complexity",
                "Don't create situation only for inputs might be that or not"
            )
        },
        {
            "role": "user",
            "content": (
                "## Pydantic Details:\n"
                f"{json.dumps(GenerateQuestions.model_json_schema(), ensure_ascii=False)}\n\n"
                "## Question :\n"
                "```json"
            )
        }
    ]