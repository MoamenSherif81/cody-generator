import inspect
import json
import time  # Import the time module

import google.generativeai as genai
from json_repair import json_repair
from tqdm import tqdm

from LLM.Queries.GenerateQuestionsQuery import GenerateMessage


def parse_json(text):
    try:
        return json_repair.loads(text)
    except:
        return None


# Array of API keys
ApiKeys = [

]

# Initialize the model (we'll configure the key within the loop)
model = genai.GenerativeModel('gemini-2.0-flash')

with open('../Examples/DslCode1.gui', 'r') as file:
    DSLCodeExample = file.read()

PromptMessage = GenerateMessage(DSLCodeExample)

prompt = ""
for i in PromptMessage:
    prompt += str(i)
    prompt += "\n"


def get_variable_name(variable):
    for name, value in inspect.currentframe().f_globals.items():
        if value == variable:
            return name
    return None


def append_json(json_file, idl, situation, Dsl, lang):
    # Creating the situation data to append to the file
    situation_data = {
        "id": idl,
        "situation": situation,
        "Dsl": Dsl,
        "lang": lang
    }
    # Write the situation data to the JSON file (appending)
    json.dump(situation_data, json_file, ensure_ascii=False, indent=4)
    json_file.write(",\n")  # Ensure each entry is on a new line


id = 1  # Start with ID 1
with open('situations.json', 'a') as json_file:
    api_key_index = 0
    successful_requests = 0
    max_requests_per_key = 14

    for i in tqdm(range(5000), desc="Processing Situations", unit="situation"):
        current_api_key = ApiKeys[api_key_index]
        genai.configure(api_key=current_api_key)

        try:
            response = model.generate_content(prompt)
            successful_requests += 1

            # Parse the JSON response
            parsed_response = parse_json(response.candidates[0].content.parts[0].text)

            if parsed_response is None:
                print("Error: Could not parse JSON response.")
                continue

            situation = parsed_response["situation"]
            SituationInArabic = situation["SituationInArabic"]
            SituationInEgyptianArabic = situation["SituationInEgyptianArabic"]
            SituationInEnglish = situation["SituationInEnglish"]
            SituationInArabicAndEnglish = situation["SituationInArabicAndEnglish"]
            Dsl = parsed_response["DslCode"]

            # Call the append_json function to store each situation with the language
            append_json(json_file, id, SituationInArabic, Dsl, "SituationInArabic")
            id += 1  # Increment id for next entry
            append_json(json_file, id, SituationInEgyptianArabic, Dsl, "SituationInEgyptianArabic")
            id += 1
            append_json(json_file, id, SituationInEnglish, Dsl, "SituationInEnglish")
            id += 1
            append_json(json_file, id, SituationInArabicAndEnglish, Dsl, "SituationInArabicAndEnglish")
            id += 1

        except Exception as e:
            # Switch to the next API key after an error
            api_key_index = (api_key_index + 1) % len(ApiKeys)
            print(f"Error encountered: {e}. Attempting to switch to the next API key.")
            time.sleep(20)

    print("\nSituations have been appended to 'situations.json'.")
    print(f"Remaining API Keys: {ApiKeys}")
