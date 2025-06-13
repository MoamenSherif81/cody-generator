import os
from typing import Optional, List

import requests
from dotenv import load_dotenv

from Ai_Agents.Agents_prompts import local_ai_answer_prompt
from Ai_Agents.AiAgent import AiAgent
from Ai_Agents.models.models import ModelMessage, ModelResponse
from LLM.Utils import parse_json


class Local(AiAgent):
    def __init__(self):
        load_dotenv()
        kaggleBaseUrl = os.getenv("KAGGLE_BASE_URL", "")
        self.url = f"{kaggleBaseUrl}/generate"

    def chat(self, message: ModelMessage, history: Optional[List[ModelMessage]] = None) -> ModelResponse:
        history = self._convert_history_to_local_ai_history(history)
        message = self._convert_message_to_local_ai_message(message)
        data = self._build_local_ai_body(history, message)
        response = requests.post(self.url, json=data)
        return parse_json(response)

    def send_message(self, message: str):
        """
        Sends a single message to the AI agent and returns the response.
        Args:
            message: The message to send.
        """
        pass

    def _build_local_ai_body(self, history, message):
        history.extend(local_ai_answer_prompt(message))
        data = {
            "message": [message.model_dump() for message in history]
        }
        return data

    def _convert_history_to_local_ai_history(self, history):
        print(type(history))
        if history is None:
            return []
        return history

    def _convert_message_to_local_ai_message(self, message):
        return message

