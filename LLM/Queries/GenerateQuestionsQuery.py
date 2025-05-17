from pydantic import json

from LLM.Scheme.GenerateQuestions import GenerateQuestions

with open('../Examples/DslCode1.gui', 'r') as file:
    DSLCodeExample = file.read()

details_extraction_messages = [
    {
        "role": "system",
        "content": "\n".join([
            "You are an Frontend Developer.",
            "Dsl Rules ={}",
            f"DSL Example={DSLCodeExample}",
            f"This is a target language (DSL) scheme{""}",
            "You have to Generate Situations JSON details according the Pydantic details.",
            "Use only Dsl Tokens.",
            "Do not generate any introduction or conclusion."
        ])
    },
    {
        "role": "user",
        "content": "\n".join([
            "## Pydantic Details:",
            json.dumps(
                GenerateQuestions.model_json_schema(), ensure_ascii=False
            ),
            "",

            "## Question :",
            "```json"
        ])
    }
]