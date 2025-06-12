import os

import google.generativeai as genai
from dotenv import load_dotenv


class Gemini:
    def __init__(self, geminiModel="gemini-2.0-flash"):
        load_dotenv()
        # Load Gemini API keys
        self.geminiKeys = os.getenv("GEMINI_API_KEY", [])
        self.geminiKeys = self.geminiKeys.split(";")
        self.numOfKeys = len(self.geminiKeys)
        self.currentKeyIdx = 0
        self.geminiModel = geminiModel
        self.model = genai.GenerativeModel(geminiModel)

    def request(self, message):
        for key in self.geminiKeys:
            try:
                genai.configure(api_key=key)
                response = self.model.generate_content(message)
                return response
            except:
                continue
        return None

# # Main loop to make requests and process responses
# for i in tqdm(range(maxNumberOfRequest)):
#     genai.configure(api_key=geminiKeys[currentKeyIdx])
#     try:
#         response = model.generate_content(PromptMessage)
#         successful_requests += 1
#
#         # Parse the JSON response
#         parsed_response = parse_json(response.candidates[0].content.parts[0].text)
#         if parsed_response is None:
#             print("Error: Could not parse JSON response.")
#             continue
#
#         dsl = parsed_response["DslCode"]
#         situation = parsed_response["situation"]
#
#         # Append responses in multiple languages
#         langs = ["SituationInArabic", "SituationInEgyptianArabic", "SituationInEnglish",
#                  "SituationInArabicAndEnglish"]
#         for lang in langs:
#             append_to_json_file(datasetPath, id, situation[lang], dsl, lang)
#     except Exception as e:
#         if numberOfRetries % maxRetries == 0:
#             sleep(sleepTime)
#         currentKeyIdx = (currentKeyIdx + 1) % numOfKeys
#         numberOfRetries += 1
