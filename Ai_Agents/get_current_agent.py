import os
from typing import Optional

from dotenv import load_dotenv

from Ai_Agents.AiAgent import AiAgent
from Ai_Agents.Gemini import Gemini
from Ai_Agents.Local import LocalModel
from Ai_Agents.OpenAi import OpenAIModel


def get_agent(agent: Optional[AiAgent] = None) -> AiAgent:
    """
    Returns the AI agent instance.
    If agent is provided, returns it.
    Otherwise, loads from environment variable 'AGENT'.
    Defaults to Gemini if not specified or unknown.
    """
    if agent is not None:
        return agent

    load_dotenv(override=True)
    agent_name = os.getenv("AGENT", "Gemini").lower()

    # Add other agent implementations here in the future
    if agent_name == "gemini":
        return Gemini()
    elif agent_name == "local":
        return LocalModel()
    elif agent_name == "openai":
        return OpenAIModel("gpt-4.1")

    return Gemini()
