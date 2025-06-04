import json
from pathlib import Path

from LLM.Scheme.GenerateQuestions import GenerateQuestions


def GenerateMessage(dsl_rules_path):
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
                "You are a Frontend Developer you want to create web page by generating website using our own custom DSL.\n"
                f"Dsl Rules = {dsl_rules}\n"
                "You have to Generate Situation JSON details according the Pydantic details.\n"
                "Use only Dsl Tokens.\n"
                "Generate Random Situation\n"
                "Do not generate any introduction or conclusion."
                "Be Creative on the situation\n"
                "Add a bit complexity\n"
                "Don't create situation only for inputs might be that or not\n"
                "Ensure all situation chars be in arabic or english only\n"
                "All the colors selected should be in the same color scheme and have good looking and harmony "
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
    prompt = ""
    for i in PromptMessage:
        prompt += str(i)
        prompt += "\n"
    return prompt


print(GenerateMessage("Queries/DSL-Rules.json"))
