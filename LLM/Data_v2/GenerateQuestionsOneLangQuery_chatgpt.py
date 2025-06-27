import json
from pathlib import Path

from LLM.Data_v2.GenerateQuestionsOneLanguage2 import ChatConversation


def GenerateMessage(dsl_rules_path, lang="arabic"):
    """
    Generate a message with DSL rules loaded from any directory.
    Args:
        dsl_rules_path (str): Path to the DSL rules file, can be absolute or relative
            to any directory (parent, sibling, child, etc.)
        lang (str): Language for the situation description, default is "arabic"

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
                "You are a creative Frontend Developer tasked with creating a dynamic, engaging, and random web page using a custom DSL.\n"
                f"Dsl Rules = {dsl_rules}\n"
                "You need to generate a highly creative, unpredictable situation based on the given Pydantic schema.\n"
                "Think outside the box and introduce unusual elements to make the situation intriguing.\n"
                "You should consider emotions, unexpected twists, environments, and characters.\n"
                "Let the situation evolve in unexpected directions, but still maintain coherence with the schema.\n"
                "The text you generate should be vibrant, lively, and add complexity, mixing elements in a fresh way.\n"
                "Do not restrict yourself to simple, static inputs. Introduce dynamic scenarios or multi-step narratives.\n"
                "Your creativity should shine through in the situation, making it engaging and potentially surprising.\n"
                "Ensure that the situation remains in either Arabic or English only.\n"
                "All colors should remain in a consistent, harmonious scheme, contributing to the visual appeal.\n"
                f"The situation description must be in language: {lang}\n"
                "For extra creativity, add some elements of conflict, unexpected resolutions, or quirky details.\n"
                "After generating the situation, return the result in **JSON format only**. Do not include any other text, explanations, or additional commentary.\n"
                "Ensure that only the JSON response is returned without any extra words.\n"
            )
        },
        {
            "role": "user",
            "content": (
                "## Pydantic Details:\n"
                f"{json.dumps(ChatConversation.model_json_schema(), ensure_ascii=False)}\n\n"
                "## Question :\n"
                "```json"
            )
        }
    ]

    return PromptMessage
