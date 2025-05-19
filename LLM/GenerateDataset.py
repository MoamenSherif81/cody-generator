import os
import sys
from time import sleep

import google.generativeai as genai
from dotenv import load_dotenv
from tqdm import tqdm

from LLM.Queries.GenerateQuestionsQuery import GenerateMessage
from LLM.Utils import append_to_json_file, write_json_data
from Utils import parse_json, load_json_data

datasetPath = "FT_Dataset/situations.json"


def main(numberOfRequests=None):
    """
    Main function to generate content using Gemini API, process it and append to a JSON dataset.

    Args:
        numberOfRequests (int, optional): The number of requests to make to the API.
                                          Defaults to None, which will calculate based on the number of API keys.
    """
    load_dotenv()

    # Load Gemini API keys
    geminiKeys = os.getenv("GEMINI_API_KEY", [])
    geminiKeys = geminiKeys.split(";")
    numOfKeys = len(geminiKeys)
    currentKeyIdx = 0

    geminiModel = "gemini-2.0-flash"
    model = genai.GenerativeModel(geminiModel)

    # Calculate the max number of requests
    maxNumberOfRequest = 1500 * numOfKeys if numberOfRequests is None else int(numberOfRequests)

    # Configure prompts
    dslRulesPath = "Queries/DSL-Rules.json"
    PromptMessage = GenerateMessage(dslRulesPath)

    # Dataset configurations
    successful_requests = 0
    maxRetries = 5
    numberOfRetries = 1
    sleepTime = 10
    id = 1
    # Main loop to make requests and process responses
    for i in tqdm(range(maxNumberOfRequest)):
        genai.configure(api_key=geminiKeys[currentKeyIdx])
        try:
            response = model.generate_content(PromptMessage)
            successful_requests += 1

            # Parse the JSON response
            parsed_response = parse_json(response.candidates[0].content.parts[0].text)
            if parsed_response is None:
                print("Error: Could not parse JSON response.")
                continue

            dsl = parsed_response["DslCode"]
            situation = parsed_response["situation"]

            # Append responses in multiple languages
            langs = ["SituationInArabic", "SituationInEgyptianArabic", "SituationInEnglish",
                     "SituationInArabicAndEnglish"]
            for lang in langs:
                append_to_json_file(datasetPath, id, situation[lang], dsl, lang)
        except Exception as e:
            if numberOfRetries % maxRetries == 0:
                sleep(sleepTime)
            currentKeyIdx = (currentKeyIdx + 1) % numOfKeys
            numberOfRetries += 1


def __main__():
    """
    This function is the entry point of the script. It calls the main processing function
    and then updates the dataset file with new IDs for each record.
    """
    if len(sys.argv) > 1:
        try:
            numberOfRequests = int(sys.argv[1])
        except ValueError:
            print("Error: The number of requests must be an integer.")
            sys.exit(1)
    else:
        # Use the default value if not passed
        numberOfRequests = None

    # Call the main function with the number of requests
    main(numberOfRequests)

    # Fix the final JSON and update the IDs
    nwId = 1
    data = load_json_data(datasetPath)
    for record in data:
        record["id"] = nwId
        nwId += 1
    write_json_data(datasetPath, data)


if __name__ == "__main__":
    __main__()
