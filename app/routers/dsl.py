from typing import List

from fastapi import APIRouter
from fastapi import UploadFile, File

from Ai_Agents import get_agent
from Ai_Agents.models.models import ModelMessage
from Compiler_V3 import safe_compile_to_web
from app.schemas.code import AnonymousCodeResponse
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
    message = ModelMessage(
        role="user",
        message=prompt
    )
    llm_response = get_agent().chat(message)
    dsl = llm_response.code
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
