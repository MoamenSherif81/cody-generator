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
        col = """body {
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
        add_products = """header <logo_color="#649ddd", title="company", args=["item 1", "item 2", "item 3"]>
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
footer <logo_color="#649ddd", title="company", args=["item1", "item2", "item3"]>
"""
        add_header = """header <logo_color="#649ddd", title="company", args=["item 1", "item 2", "item 3"]>
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
        add_side_nav = """
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
        from time import sleep
        if message.message.startswith("add"):
            sleep(0.9)
            return True, ModelResponse(message="added", code=add_side_nav)
        if message.message.startswith("m"):
            sleep(0.6)
            return True, ModelResponse(message="ok", code=col)
        if message.message.startswith("a"):
            sleep(0.7)
            return True, ModelResponse(message="added", code=add_header)
        if message.message.startswith("i"):
            sleep(0.2)
            return True, ModelResponse(message="added", code=add_products)

        return False, None

