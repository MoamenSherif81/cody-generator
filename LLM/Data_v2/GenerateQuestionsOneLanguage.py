from typing import Literal, List
from pydantic import BaseModel, Field

# class Situation(BaseModel):
#     description: str = Field(...,
#                              description="Description of the web page or scenario being created. For example, a description of a login page or a feature to be implemented.",
#                              examples=["I want to create a login page", "Please add a registration form"])

class MessageHistory(BaseModel):
    role: Literal["user", "system"] = Field(...,
                                             description="Indicates whether the sender is the user or the system.")
    content: str = Field(...,
                         description="The content of the message. If the sender is the user, this will contain the user's question. If the sender is the system, this will contain the system's response.")
    code: str = Field(...,
                      description="If the sender is the user, this will contain the code sent to the system. If the sender is the system, this will contain the system's response to the user's input.")

class GeneratedQuestion(BaseModel):
    id: int = Field(...,
                    description="Unique identifier for the question or the set of generated questions.")
    question: str = Field(...,
                                 description="if the history is empty so it's the user initial command  to generate website page"
                                             "if there is history so it's a user follow ")
    response: str = Field(...,
                          description="The model's response to the user's question or the situation described.",
                          examples=["Here is what you asked, I added a button to the current page"])
    dsl_code: str = Field(...,
                          description="The corresponding DSL code that matches the situation and response.")
    lang: Literal["ar", "en"] = Field(...,
                                      description="The language in which the DSL code and situation description are written. It can be either 'ar' (Arabic) or 'en' (English).")
    history: List[MessageHistory] = Field(...,
                                          description="The history of messages exchanged between the user and the system during the interaction. This includes both the user's questions and the system's responses.",
                                          min_length=6, max_length=10)
