from typing import List

from fastapi import APIRouter
from fastapi import UploadFile, File

from Compiler_V3 import safe_compile_to_web
from LLM.Utils import parse_json
from app.schemas.code import AnonymousCodeResponse
from app.schemas.message import LLmMessageFormat
from app.services.KaggleService import LLMService
from app.services.ai_service import process_screenshots

router = APIRouter(prefix="/dsl", tags=["dsl"])


@router.post(
    "/image",
    summary="Create a record with a screenshot",
    description="Upload one or more screenshot images.",
    response_description="The created record object with screenshot_path as a URL.",
    response_model=AnonymousCodeResponse
)
async def create_image_record(
        screenshots: List[UploadFile] = File(...),
):
    dsl = await process_screenshots(screenshots)
    return AnonymousCodeResponse.from_dsl(dsl)


@router.post(
    "/text",
    summary="Create a record with DSL content",
    description="Create a record with mandatory DSL content, returns compiled HTML & CSS.",
    response_model=AnonymousCodeResponse
)
async def create_dsl_record(
        dsl_content: str,
):
    return AnonymousCodeResponse.from_dsl(dsl_content)


@router.post(
    "/prompt",
    summary="Create a record with DSL content",
    description="Create a record with mandatory DSL content, returns compiled HTML & CSS.",
    response_model=AnonymousCodeResponse
)
async def create_dsl_record(
        prompt: str,
):
    llm_service = LLMService()
    message = LLmMessageFormat(
        role="user",
        content=prompt
    )
    llm_response = llm_service.GenerateResponse(message, [])["response"]
    dsl = parse_json(llm_response)['dsl']
    return AnonymousCodeResponse.from_dsl(dsl)


@router.post(
    "/lint",
    response_model=AnonymousCodeResponse,
    summary="Create a record with DSL content",
    description="Create a record with mandatory DSL content, associated with the authenticated user. Project ID is optional. Requires a valid JWT token (Bearer <token>) in the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The created record object."
)
async def create_dsl_record(
        dsl_content: str,
):
    _, _ = safe_compile_to_web(dsl_content)
    return AnonymousCodeResponse.from_dsl(dsl_content)
