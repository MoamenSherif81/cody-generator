import os
from typing import List, Optional

from dotenv import load_dotenv
from google import genai

from Ai_Agents.AiAgent import AiAgent
from Ai_Agents.models.models import ModelMessage, ModelResponse


class Gemini(AiAgent):
    def __init__(self, geminiModel="gemini-1.5-flash"):
        load_dotenv()
        self.geminiKeys = [key.strip() for key in os.getenv("GEMINI_API_KEY", "").split(";") if key.strip()]
        if not self.geminiKeys:
            raise ValueError("GEMINI_API_KEY environment variable not found or is empty.")
        self.numOfKeys = len(self.geminiKeys)
        self.currentKeyIdx = 0
        self.geminiModel = geminiModel
        self.client = genai.Client()

    def _convert_message_to_gemini_content(self, msg: ModelMessage) -> genai.types.Content:
        parts = []
        if msg.message:
            # Here, genai.types.Part.from_text() is used correctly
            parts.append(genai.types.Part.from_text(msg.message))
        if msg.code:
            parts.append(genai.types.Part.from_text(f"```\n{msg.code}\n```"))
        return genai.types.Content(parts=parts, role=msg.role)

    def chat(self, message: ModelMessage, history: Optional[List[ModelMessage]] = None) -> ModelResponse:
        full_contents = [
            {
                "role": "user",
                "parts": [
                    {
                        "text": "List a few popular cookie recipes, and include the amounts of ingredients."
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": (
                            "Here are a few popular cookie recipes:\n\n"
                            "1. **Chocolate Chip Cookies**\n"
                            "   - 1 cup (2 sticks) unsalted butter, softened\n"
                            "   - 3/4 cup granulated sugar\n"
                            "   - 3/4 cup packed light brown sugar\n"
                            "   - 2 large eggs\n"
                            "   - 1 teaspoon vanilla extract\n"
                            "   - 2 1/4 cups all-purpose flour\n"
                            "   - 1 teaspoon baking soda\n"
                            "   - 1/2 teaspoon salt\n"
                            "   - 2 cups (12 oz) semi-sweet chocolate chips\n\n"
                            "2. **Oatmeal Raisin Cookies**\n"
                            "   - 1 cup (2 sticks) unsalted butter, softened\n"
                            "   - 1 cup packed light brown sugar\n"
                            "   - 1/2 cup granulated sugar\n"
                            "   - 2 large eggs\n"
                            "   - 1 teaspoon vanilla extract\n"
                            "   - 1 1/2 cups all-purpose flour\n"
                            "   - 1 teaspoon baking soda\n"
                            "   - 1 teaspoon cinnamon\n"
                            "   - 1/2 teaspoon salt\n"
                            "   - 3 cups old-fashioned rolled oats\n"
                            "   - 1 1/2 cups raisins"
                        )
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": "Now, from those, can you list only the chocolate cookie recipes?"
                    }
                ]
            }
        ]

        for key in self.geminiKeys:
            try:
                # self.client._api_client.api_key = key
                self.client = genai.Client(api_key=key)
                raw_response = self.client.models.generate_content(
                    model=self.geminiModel,
                    contents=full_contents,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": ModelResponse,
                    },
                )
                return raw_response.parsed
            except Exception as e:
                print(f"Error with key (last 5 chars): ...{key[-5:]}: {e}")
                continue

        print("All Gemini API keys failed.")
        return ModelResponse(message="Error: All Gemini API keys failed to get a response.")

    def send_message(self, message: str) -> ModelResponse:
        msg = ModelMessage(role="user", message=message, code="")
        return self.chat(msg, history=None)
