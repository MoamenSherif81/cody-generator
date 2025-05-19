import json
from pathlib import Path
from tkinter.messagebox import askquestion

from LLM.Scheme.AnswerQuestion import AnswerQuestion, AskQuestion
from LLM.Scheme.GenerateQuestions import GenerateQuestions


def AnswerPrompt(dsl_rules_path,prom):
    """
    Generate a message with DSL rules loaded from any directory.
    Args:
        dsl_rules_path (str): Path to the DSL rules file, can be absolute or relative
            to any directory (parent, sibling, child, etc.)

    Returns:
        list: Message components with DSL rules included
    """
    # Convert to absolute path if it's not already
    abs_path = Path(dsl_rules_path).resolve()

    # Check if file exists
    if not abs_path.exists():
        raise FileNotFoundError(f"DSL rules file not found: {abs_path}")

    # Read the DSL rules
    with open(abs_path, 'r') as file:
        dsl_rules = file.read()

    PromptMessage = [
        {
            "role": "system",
            "content": (
                "You are a professional Frontend Developer that can generate webpage using our own custom DSL.\n"
                "Generate the dsl for the provided situation"
                f"Dsl Rules = {dsl_rules}\n"
                f"You have to Generate response JSON {json.dumps(AnswerQuestion.model_json_schema(), ensure_ascii=False)} according the Pydantic details.\n"
                "Use only Dsl Tokens.\n"
                "Do not generate any introduction or conclusion."
                "Use a simple, visually appealing random color scheme, ensuring all selected colors belong to it."
                "don't give color to text or title token"
                "Be Creative"
            )
        },
        {
            "role": "user",
            "content": (
                "## Pydantic Details:\n"
                f"{json.dumps(AskQuestion.model_json_schema(), ensure_ascii=False)}\n\n"
                f"## Question :\n {prom} \n"
                "```json"
            )
        }
    ]
    prompt = ""
    for i in PromptMessage:
        prompt += str(i)
        prompt += "\n"
    return prompt
print(AnswerPrompt("DSL-Rules.json"," i want to make questionnaire form "))