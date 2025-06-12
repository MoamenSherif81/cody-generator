from abc import ABC, abstractmethod
from typing import List, Optional

from Ai_Agents.models.models import ModelMessage, ModelResponse


class AiAgent(ABC):
    @abstractmethod
    def chat(self, message: ModelMessage, history: Optional[List[ModelMessage]] = None) -> ModelResponse:
        """
        Sends a message to the AI agent and returns the response.
        Args:
            message: The current user or system message.
            history: Optional list of previous ModelMessages for chat history.
        Returns:
            ModelResponse: The agent's response.
        """
        pass

    def send_message(self, message: str):
        """
        Sends a single message to the AI agent and returns the response.
        Args:
            message: The message to send.
        """
        pass
