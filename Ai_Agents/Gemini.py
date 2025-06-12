import os
from typing import List, Optional

import google.generativeai as genai
from dotenv import load_dotenv

from Ai_Agents.AiAgent import AiAgent
from Ai_Agents.models.models import ModelMessage, ModelResponse


class Gemini(AiAgent):
    """
    Gemini AI agent for Google Generative AI chat interface.
    """

    def __init__(self, geminiModel="gemini-2.5-flash"):
        """
        Load API keys from environment and set up the Gemini model.
        """
        load_dotenv()
        self.geminiKeys = [key.strip() for key in os.getenv("GEMINI_API_KEY", "").split(";") if key.strip()]
        if not self.geminiKeys:
            raise ValueError("GEMINI_API_KEY environment variable not found or is empty.")
        self.numOfKeys = len(self.geminiKeys)
        self.currentKeyIdx = 0
        self.geminiModel = geminiModel
        self.model = genai.GenerativeModel(geminiModel)

    def chat(self, message: ModelMessage, history: Optional[List[ModelMessage]] = None) -> ModelResponse:
        """
        Send a message and history to Gemini and return the response.
        Tries all API keys until one succeeds.
        """
        gemini_history = self._convert_history_to_gemini_history(history)
        gemini_message = self._convert_message_to_gemini_message(message)
        for key in self.geminiKeys:
            try:
                genai.configure(api_key=key)
                chat = self.model.start_chat(history=gemini_history)
                if not gemini_message:
                    raise ValueError("Converted message is empty, cannot send to Gemini.")
                response = chat.send_message(gemini_message)
                return self._convert_gemini_response_to_model_response(response)
            except Exception as e:
                print(f"Error with key (last 5 chars): ...{key[-5:]}: {e}")
                continue
        print("All Gemini API keys failed.")
        return ModelResponse(message="Error: All Gemini API keys failed to get a response.")

    def send_message(self, message: str):
        """
        Send a single message (no history) to Gemini and get the response.
        """
        msg = ModelMessage(role="user", message=message)
        return self.chat(msg, history=None)

    def _convert_message_to_gemini_message(self, message: ModelMessage):
        """
        Change ModelMessage to Gemini's format (list of message parts).
        """
        parts = []
        if message.message:
            parts.append(message.message)
        if message.code:
            parts.append(f"```DSL\n{message.code}\n```")
        if not parts:
            return None
        return parts

    def _convert_history_to_gemini_history(self, history: Optional[List[ModelMessage]] = None):
        """
        Change a list of ModelMessage to Gemini's chat history format.
        """
        if history is None:
            return []
        gemini_formatted_history = []
        for msg in history:
            content_parts = []
            if msg.message:
                content_parts.append(msg.message)
            if msg.code:
                content_parts.append(f"```\n{msg.code}\n```")
            gemini_role = "user" if msg.role == "user" else "model"
            gemini_formatted_history.append({"role": gemini_role, "parts": content_parts})
        return gemini_formatted_history

    def _convert_gemini_response_to_model_response(self, gemini_response) -> ModelResponse:
        """
        Change Gemini API response to ModelResponse.
        Splits text and code if present.
        """
        full_message = []
        full_code = []
        if gemini_response and hasattr(gemini_response, "candidates"):
            for candidate in gemini_response.candidates:
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'text'):
                            text_content = part.text
                            if text_content.startswith('```') and text_content.endswith('```'):
                                full_code.append(text_content.strip('`').strip())
                            else:
                                full_message.append(text_content)
        response_message = "\n".join(full_message) if full_message else None
        response_code = "\n".join(full_code) if full_code else None
        return ModelResponse(message=response_message, code=response_code)
