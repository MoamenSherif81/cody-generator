import json
import os

from dotenv import load_dotenv

from LLM.Data_v2.GenerateQuestionsOneLangQuery_chatgpt import GenerateMessage
from LLM.Utils import parse_json
load_dotenv()
# Load Gemini API keys
geminiKeys = os.getenv("GEMINI_API_KEY", [])
geminiKeys = geminiKeys.split(";")
# Generate the JSON data
x = GenerateMessage("/home/mohab/Mohab/GP/cody-generator/LLM/Queries/DSL-Rules.json","english")

for i in x :
    print(i)
# import google.generativeai as genai
#
# # Configure your API key
# genai.configure(api_key=geminiKeys[0])
#
# # Get the Gemini model you want to use
# model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20') # Or 'gemini-1.5-pro' or another suitable model
# messages =x
# response = model.generate_content(messages)
#
#
# # Print the response from Gemini
# print(response.text)