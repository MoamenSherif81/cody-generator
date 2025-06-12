import os
from typing import Optional
from dotenv import load_dotenv

from Ai_Agents.AiAgent import AiAgent
from Ai_Agents.Gemini import Gemini

def get_agent(agent: Optional[AiAgent] = None) -> AiAgent:
    """
    Returns the AI agent instance.
    If agent is provided, returns it.
    Otherwise, loads from environment variable 'AGENT'.
    Defaults to Gemini if not specified or unknown.
    """
    if agent is not None:
        return agent

    load_dotenv()
    agent_name = os.getenv("AGENT", "Gemini").lower()

    # Add other agent implementations here in the future
    if agent_name == "gemini":
        return Gemini()
    # elif agent_name == "openai":
    #     return OpenAIAgent()
    # Add more agents as needed

    # Default fallback
    return Gemini()
