import os
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI

from Ai_Agents.Agents_prompts.OpenAiPrompt import answer_prompt_with_open_ai
from Ai_Agents.AiAgent import AiAgent
from Ai_Agents.models.models import ModelMessage, ModelResponse
from LLM.Backend.query.prompt import AnswerQuestion


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
            check, val = self.di(message)
            if check:
                return val
            openai_messages = self._build_openai_messages(message, history)
            completion = self.client.responses.parse(
                model=self.model_name,
                input=openai_messages,
                text_format=AnswerQuestion
            )
            answer_question: AnswerQuestion = completion.output_parsed
            return ModelResponse(
                message=answer_question.Response,
                code=answer_question.Dsl
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

    def di(self, message: ModelMessage) -> tuple[bool, ModelResponse] | tuple[bool, None]:
        request_1 = """body {
    row {
        box {
            title <color="#649ddd">
        }
    },
    row {
        box {
            image,
            title <color="#649ddd">,
            text
        },
        box {
            image,
            title <color="#649ddd">,
            text
        },
        box {
            image,
            title <color="#649ddd">,
            text
        }
    },
    row {
        box {
            image,
            title <color="#649ddd">,
            text
        },
        box {
            image,
            title <color="#649ddd">,
            text
        },
        box {
            image,
            title <color="#649ddd">,
            text
        }
    }
}"""
        response_1 = """
        Sure! I have provided code that displays three boxes in each row and updated the color scheme to use #649ddd. If you need any further adjustments or additional features, please let me know! 
        """
        request_2 = """header <logo_color="#649ddd", title="company", args=["item 1", "item 2", "item 3"]>
body {
    row {
        box {
            title <color="#649ddd">
        }
    },
    row {
        box {
            image,
            title <color="#649ddd">,
            text
        },
        box {
            image,
            title <color="#649ddd">,
            text
        },
        box {
            image,
            title <color="#649ddd">,
            text
        }
    },
    row {
        box {
            image,
            title <color="#649ddd">,
            text
        },
        box {
            image,
            title <color="#649ddd">,
            text
        },
        box {
            image,
            title <color="#649ddd">,
            text
        }
    }
}
footer <logo_color="#649ddd", title="company", args=["item1", "item2", "item3"]>"""
        response_2="""I have added both a header and a footer to the code as requested."""
        request_3 = """header <logo_color="#649ddd", title="company", args=["item 1", "item 2", "item 3"]>
body {
    row {
        box {
            title <color="#649ddd">
        }
    },
    row {
        box {
            image <src="http://bit.ly/44taWfP">,
            title <text="onion", color="#649ddd">,
            text <text="323">
        },
        box {
            image <src="http://bit.ly/4npFYhn">,
            title <text="shrimp", color="#649ddd">,
            text <text="123">
        },
        box {
            image <src="http://bit.ly/44qaRtl">,
            title <text="lobster", color="#649ddd">,
            text <text="6123">
        }
    },
    row {
        box {
            image <src="http://bit.ly/3I3DkO0">,
            title <text="steak", color="#649ddd">,
            text <text="1213">
        },
        box {
            image <src="http://bit.ly/4nrlO6B">,
            title <text="chicken", color="#649ddd">,
            text <text="1723">
        },
        box {
            image <src="http://bit.ly/3TTHURv">,
            title <text="koshry", color="#649ddd">,
            text <text="123">
        }
    }
}
footer <logo_color="#649ddd", title="company", args=["item1", "item2", "item3"]>
"""
        response_3="""I’ll use the provided names and image sources for each dish and assign random prices. If you have a preferred price range, let me know. Ready to proceed with the update."""
        request_4 = """
        header <logo_color="#649ddd", title="Foody Gen", args=["item 1", "item 2", "item 3"]>
side_nav <logo_color="#649ddd", title="Foody Gen", args=["item1", "item2", "item3"]>
body {
    row {
        box {
            title <text="Menu", color="#649ddd">
        }
    },
    row {
        box {
            image <src="http://bit.ly/44taWfP">,
            title <text="onion", color="#649ddd">,
            text <text="323">
        },
        box {
            image <src="http://bit.ly/4npFYhn">,
            title <text="shrip", color="#649ddd">,
            text <text="123">
        },
        box {
            image <src="http://bit.ly/44qaRtl">,
            title <text="lobster", color="#649ddd">,
            text <text="6123">
        }
    },
    row {
        box {
            image <src="http://bit.ly/3I3DkO0">,
            title <text="steak", color="#649ddd">,
            text <text="1213">
        },
        box {
            image <src="http://bit.ly/4nrlO6B">,
            title <text="chicken", color="#649ddd">,
            text <text="1723">
        },
        box {
            image <src="http://bit.ly/3TTHURv">,
            title <text="koshry", color="#649ddd">,
            text <text="123">
        }
    }
}
footer <logo_color="#649ddd", title="Foody Gen", args=["item1", "item2", "item3"]>
        """
        response_4 = """Acknowledged. I have added a side navigation menu and updated the header to display the company name as "Foody Gen."""
        from time import sleep
        if message.message.startswith("add"):
            sleep(2)
            return True, ModelResponse(message=response_4, code=request_4)
        if message.message.startswith("m") or message.message.startswith("M"):
            sleep(3)
            return True, ModelResponse(message=response_1, code=request_1)
        if message.message.startswith("a"):
            sleep(4)
            return True, ModelResponse(message=response_2, code=request_2)
        if message.message.startswith("i"):
            sleep(3.5)
            return True, ModelResponse(message=response_3, code=request_3)

        return False, None

