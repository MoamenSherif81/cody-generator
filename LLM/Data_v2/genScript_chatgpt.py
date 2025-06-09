from openai import OpenAI

client = OpenAI(api_key='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')
import json
from LLM.Data_v2.GenerateQuestionsOneLangQuery_chatgpt import GenerateMessage

print(GenerateMessage("/home/mohab/Mohab/GP/cody-generator/LLM/Queries/DSL-Rules.json","english"))