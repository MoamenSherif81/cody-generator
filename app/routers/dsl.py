from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse

from Compiler_V2 import lint_dsl, compile_dsl
from app.schemas.record import RecordResponse
from app.services.ai_service import process_screenshots

router = APIRouter(prefix="/dsl", tags=["dsl"])

from fastapi import APIRouter, UploadFile, File
from typing import List
from fastapi.responses import JSONResponse

@router.post(
    "/image",
    summary="Create a record with a screenshot",
    description="Upload one or more screenshot images.",
    response_description="The created record object with screenshot_path as a URL.",
)
async def create_image_record(
    screenshot: List[UploadFile] = File(...),
):
    dsl, html, css = process_screenshots(screenshot)
    dsl = lint_dsl(dsl)
    return JSONResponse(content={
        "html": html,
        "css": css,
        "dsl": dsl
    })

from app.schemas.dsl import DSLContentRequest

@router.post(
    "/text",
    summary="Create a record with DSL content",
    description="Create a record with mandatory DSL content, returns compiled HTML & CSS.",
)
async def create_dsl_record(
        body: DSLContentRequest,
):
    dsl_content = body.dsl_content
    if not dsl_content.strip():
        raise HTTPException(
            status_code=400,
            detail="dsl_content must not be empty"
        )

    html, css = compile_dsl(dsl_content)
    dsl_content = lint_dsl(dsl_content)
    return JSONResponse(content={
        "html": html,
        "css": css,
        "dsl": dsl_content
    })

@router.post(
    "/lint",
    response_model=RecordResponse,
    summary="Create a record with DSL content",
    description="Create a record with mandatory DSL content, associated with the authenticated user. Project ID is optional. Requires a valid JWT token (Bearer <token>) in the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The created record object."
)
async def create_dsl_record(
        dsl_content: str,
):
    if not dsl_content.strip():
        raise HTTPException(
            status_code=400,
            detail="dsl_content must not be empty"
        )

    html, css = compile_dsl(dsl_content)
    dsl_content = lint_dsl(dsl_content)
    return JSONResponse(content={
        "html": html,
        "css": css,
        "dsl": dsl_content
    })
