import os
import google.generativeai as genai

from Compiler_V2 import lint_dsl, compile_dsl
from LLM.Queries.GenerateQuestionsOneLangQuery import GenerateMessage
from LLM.Utils import parse_json
from app.schemas.Situation.GenerateSituation import GenerateSituation
from app.schemas.Situation.GetSituation import GetSituation

from fastapi import HTTPException, status

async def Generate_Situation(generate_situation: GenerateSituation) -> GetSituation:
    """
    Generates a situation based on user input using the Gemini AI model.
    1. Loads API keys and initializes the model.
    2. Sends a prompt to the AI model.
    3. Parses and validates the AI response.
    4. Compiles DSL to HTML/CSS.
    5. Maps results to GetSituation schema and returns it.
    """
    gemini_keys = os.getenv("GEMINI_API_KEY", "")
    if not gemini_keys:
        raise RuntimeError("No GEMINI_API_KEY found in environment variables.")
    gemini_keys = gemini_keys.split(";")

    # Model selection
    try:
        model = genai.GenerativeModel(generate_situation.model)
    except Exception as ex:
        raise RuntimeError(f"Error initializing Gemini model: {ex}")

    dsl_rules_path = "LLM/Queries/DSL-Rules.json"
    prompt_message = GenerateMessage(dsl_rules_path, generate_situation.language)

    response = None
    for key in gemini_keys:
        try:
            genai.configure(api_key=key)
            ai_response = model.generate_content(prompt_message)
            parsed = parse_json(ai_response.candidates[0].content.parts[0].text)
            if not parsed:
                continue  # Try next key if parsing fails
            response = parsed
            break
        except Exception as ex:
            print("Failed to fetch with Gemini key ")
            continue  # Log or handle per-key errors if needed

    if not response:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to get a valid response from Gemini API."
        )

    # Parse DSL and situation description
    try:
        dsl_code = response["DslCode"]
        situation_desc = response["situation"]["SituationDescription"]
        # If dsl_code is a string with unwanted braces, clean and try to parse again
        if isinstance(dsl_code, str) and dsl_code.startswith("{") and dsl_code.endswith("}"):
            try:
                cleaned = dsl_code[1:-1]  # remove first and last character
                dsl_code = cleaned
            except Exception as ex2:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Malformed DSL code after removing braces: {ex2}"
                )
    except KeyError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Missing expected keys in AI response: {ex}"
        )

    try:
        linted_dsl = lint_dsl(dsl_code)
        html, css = compile_dsl(dsl_code)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error compiling DSL: {ex}"
        )

    # Build response model
    return GetSituation(
        situationDescription=situation_desc,
        html=html,
        dsl=linted_dsl,
        css=css,
        language=generate_situation.language,
        aiModel=generate_situation.model
    )
