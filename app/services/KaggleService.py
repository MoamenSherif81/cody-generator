# import json
# import os
#
# import requests
# from dotenv import load_dotenv
#
# from LLM.Scheme.AnswerQuestion import AskQuestion, AnswerQuestion
# from app.schemas.message import LLmMessageFormat
#
# load_dotenv()
#
#
# class LLMService:
#     _dsl_rules = os.path.join(os.getcwd(), "LLM/Queries/DSL-Rules.json")
#
#     def GenerateResponse(self, message:str, history=None):
#         if history is None:
#             history = []
#         kaggleBaseUrl = os.getenv("KAGGLE_BASE_URL", "")
#         url = f"{kaggleBaseUrl}/generate"
#         print(url)
#         if history is None:
#             history = []
#         history.extend(self._AnswerPrompt(message))
#         data = {
#             "message": [message.model_dump() for message in history]
#         }
#         print(data)
#         response = requests.post(url, json=data)
#         print(response)
#         return response.json()
#
#     def _AnswerPrompt(self, prom:str):
#         with open(self._dsl_rules, 'r') as file:
#             dsl_rules = file.read()
#
#         PromptMessage = [
#             LLmMessageFormat(
#                 role="system",
#                 content=(
#                     "You are a professional Frontend Developer that can generate webpage using our own custom DSL.\n"
#                     "Generate the dsl for the provided situation"
#                     f"Dsl Rules = {dsl_rules}\n"
#                     f"You have to Generate response JSON {json.dumps(AnswerQuestion.model_json_schema(), ensure_ascii=False)} according the Pydantic details.\n"
#                     "Use only Dsl Tokens.\n"
#                     "Do not generate any introduction or conclusion."
#                     "Use a simple, visually appealing random color scheme, ensuring all selected colors belong to it."
#                     "don't give color to text or title token"
#                     "Be Creative"
#                 ))
#             ,
#             LLmMessageFormat(
#                 role="user",
#                 content=(
#                     "## Pydantic Details:\n"
#                     f"{json.dumps(AskQuestion.model_json_schema(), ensure_ascii=False)}\n\n"
#                     f"## Question :\n {prom} \n"
#                     "```json"
#                 )
#             )
#
#         ]
#         return PromptMessage
