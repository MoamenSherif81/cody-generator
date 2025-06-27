from typing import Optional, List

from fastapi import APIRouter, Depends, UploadFile, File, Body
from fastapi import Form
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.record import UpdateRecord, GetRecordResponse, GetAllRecordResponse
from app.services.RecordService import RecordService

router = APIRouter(prefix="/records", tags=["Records"])


def get_record_service(db: Session = Depends(get_db), current_user: User = Depends(get_current_user, use_cache=False)):
    return RecordService(db, current_user)


@router.post(
    "/image",
    summary="Create a record with screenshots",
    description="Upload one or more screenshot images to generate DSL, HTML, and CSS. Optionally save to database with project ID and user authentication. Requires a valid JWT token for authenticated requests.",
    response_description="The created record object (if saved) with screenshot_path as a URL, and compiled HTML, CSS, and DSL.",
    response_model=GetRecordResponse
)
async def create_image_record(
        screenshots: List[UploadFile] = File(...),
        project_id: Optional[int] = Form(None),
        service: RecordService = Depends(get_record_service),

):
    return await service.create_image_record(screenshots, project_id)


@router.post(
    "/dsl",
    summary="Create a record with DSL content",
    description="Create a record with mandatory DSL content, associated with the authenticated user. Project ID is optional. Requires a valid JWT token (Bearer <token>).",
    response_description="The created record object.",
    response_model=GetRecordResponse

)
async def create_dsl_record(
        dsl_content: str = Body(...),
        project_id: Optional[int] = None,
        service: RecordService = Depends(get_record_service),
):
    return service.create_dsl_record(dsl_content, project_id)


@router.post(
    "/prompt",
    summary="Create a record with prompt",
    description="Create a record with prompt. Project ID is optional. Requires a valid JWT token (Bearer <token>).",
    response_model=GetRecordResponse

)
async def create_prompt_record(
        dsl_content: str = Body(...),
        project_id: Optional[int] = None,
        service: RecordService = Depends(get_record_service),
):
    return service.create_prompt_record(dsl_content, project_id)


@router.get(
    "/all",
    summary="Get all records with no project",
    description="Retrieve all records that have no project_id, belonging to the authenticated user. Ordered ascending by creation date.",
    response_description="A list of record objects including record_id.",
    response_model=GetAllRecordResponse
)
def get_records_no_project(
        service: RecordService = Depends(get_record_service),
):
    return service.get_records_with_no_project()


@router.get(
    "/{record_id}",
    summary="Get a record by ID",
    description="Retrieve a specific record by its ID, only if it belongs to the authenticated user. Compiles DSL to HTML and CSS.",
    response_description="The record object with compiled HTML and CSS.",
    response_model=GetRecordResponse
)
def get_record_by_id(
        record_id: int,
        service: RecordService = Depends(get_record_service),
):
    return service.get_single_record(record_id)


@router.put(
    "/{record_id}",
    summary="Update DSL content of a record",
    description="Update the DSL content of a record by its ID. The record must belong to the authenticated user. DSL will be compiled to HTML and CSS. Requires a valid JWT token (Bearer <token>).",
    response_description="The updated record object with compiled HTML and CSS.",
    response_model=GetRecordResponse
)
def update_record_dsl(
        record_id: int,
        record: UpdateRecord,
        service: RecordService = Depends(get_record_service),
):
    return service.update_record(record_id, record)


@router.delete(
    "/{record_id}",
    summary="Delete a record",
    description="Delete a record by its ID, belonging to the authenticated user. If the record has a screenshot, the file is removed from the uploads directory. Requires a valid JWT token (Bearer <token>).",
    response_description="Confirmation of record deletion."
)
def delete_record(
        record_id: int,
        service: RecordService = Depends(get_record_service),
):
    return service.delete_record(record_id)
