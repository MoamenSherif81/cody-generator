import os
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI

from Ai_Agents.Agents_prompts.OpenAiPrompt import answer_prompt_with_open_ai
from Ai_Agents.AiAgent import AiAgent
from Ai_Agents.models.models import ModelMessage, ModelResponse
from LLM.Utils import parse_json


class OpenAIModel(AiAgent):
    def __init__(self, model_name="gpt-4o"):
        load_dotenv()
        api_key = os.getenv("OPENAI_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_KEY environment variable not found.")
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def chat(self, message: ModelMessage, history: Optional[List[ModelMessage]] = None) -> ModelResponse:
        """
        Sends message + history to OpenAI and returns parsed response.
        """
        try:
            openai_messages = self._build_openai_messages(message, history)
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=openai_messages
            )
            content = completion.choices[0].message.content
            parsed = parse_json(content)
            return ModelResponse(
                message=parsed.get("Response"),
                code=parsed.get("Dsl")
            )
        except Exception as e:
            print(f"OpenAI error: {e}")
            return ModelResponse(message="Error with OpenAI API.", code=None)

    def send_message(self, message: str) -> ModelResponse:
        """
        Sends a plain message to OpenAI without history.
        """
        msg = ModelMessage(role="user", message=message)
        return self.chat(msg)

    def _build_openai_messages(self, message: ModelMessage, history: Optional[List[ModelMessage]] = None):
        """
        Convert ModelMessage + history to OpenAI-compatible message list.
        """
        history = history or []
        messages = []

        for msg in history:
            content = []
            if msg.message:
                content.append(msg.message)
            if msg.code:
                content.append(f"```DSL\n{msg.code}\n```")
            full_content = "\n".join(content)
            messages.append({
                "role": msg.role,
                "content": full_content
            })
        content = []
        if message.message:
            content.append(answer_prompt_with_open_ai(message.message))
        if message.code:
            content.append(f"```DSL\n{msg.code}\n```")
        full_content = "\n".join(content)
        messages.append({
            "role": message.role,
            "content": full_content
        })

        return messages
