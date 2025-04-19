import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi import Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from Compiler_V2 import lint_dsl, compile_dsl
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.record import Record, RecordListResponse
from app.models.user import User
from app.schemas.record import RecordResponse
from app.services.ai_service import process_screenshot

router = APIRouter(prefix="/records", tags=["Records"])


@router.post(
    "/image",
    response_model=RecordResponse,
    summary="Create a record with a screenshot",
    description="Create a record with a mandatory screenshot, associated with the authenticated user. The screenshot is saved and accessible via /uploads/<filename>. Project ID is optional. Requires a valid JWT token (Bearer <token>) in the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The created record object with screenshot_path as a URL."
)
async def create_image_record(
        screenshot: UploadFile = File(...),
        project_id: int = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Handle file upload
    filename = f"{datetime.utcnow().timestamp()}_{screenshot.filename}"
    file_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(screenshot.file.read())
    screenshot_url = f"/uploads/{filename}"
    dsl, html, css = process_screenshot(screenshot)
    db_record = Record(
        screenshot_path=screenshot_url,
        dsl_content=dsl,
        user_id=current_user.id,
        project_id=project_id,
        created_at=datetime.utcnow()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return JSONResponse(content={
        "record": {
            "id": db_record.id,
            "screenshot_path": db_record.screenshot_path,
            "dsl_content": db_record.dsl_content,
            "user_id": db_record.user_id,
            "project_id": db_record.project_id,
            "created_at": db_record.created_at.isoformat()
        },
        "compiled_html": html,
        "compiled_css": css
    })


@router.post(
    "/dsl",
    response_model=RecordResponse,
    summary="Create a record with DSL content",
    description="Create a record with mandatory DSL content, associated with the authenticated user. Project ID is optional. Requires a valid JWT token (Bearer <token>) in the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The created record object."
)
async def create_dsl_record(
        dsl_content: str,
        project_id: int = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Validate dsl_content
    if not dsl_content.strip():
        raise HTTPException(
            status_code=400,
            detail="dsl_content must not be empty"
        )

    # Create record
    html, css = compile_dsl(dsl_content)
    dsl_content = lint_dsl(dsl_content)
    db_record = Record(
        screenshot_path=None,
        dsl_content=dsl_content,
        user_id=current_user.id,
        project_id=project_id,
        created_at=datetime.utcnow()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return JSONResponse(content={
        "record": {
            "id": db_record.id,
            "screenshot_path": db_record.screenshot_path,
            "dsl_content": db_record.dsl_content,
            "user_id": db_record.user_id,
            "project_id": db_record.project_id,
            "created_at": db_record.created_at.isoformat()
        },
        "compiled_html": html,
        "compiled_css": css
    })


@router.get(
    "/all",
    response_model=RecordListResponse,
    summary="Get all records with no project",
    description="Retrieve all records that have no project_id, belonging to the authenticated user. Ordered ascending by creation date.",
    response_description="A list of record objects."
)
def get_records_no_project(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Query records with no project_id for the authenticated user, ordered by created_at ascending
    records = (
        db.query(Record)
        .filter(Record.user_id == current_user.id, Record.project_id.is_(None))
        .order_by(Record.created_at.asc())
        .all()
    )

    # If no records are found, return an empty list
    if not records:
        return {"data": []}

    # Prepare response data
    response_data = []
    for record in records:
        # Compile DSL content to HTML and CSS, handle None case
        html, css = compile_dsl(record.dsl_content) if record.dsl_content else (None, None)
        response_data.append({
            "record_id": record.id,
            "screenshotPath": record.screenshot_path,
            "dsl_code": record.dsl_content,
            "Html": html,
            "Css": css
        })

    return {"data": response_data}


@router.delete(
    "/{record_id}",
    summary="Delete a record",
    description="Delete a record by its ID, belonging to the authenticated user. If the record has a screenshot, the file is removed from the uploads directory. Requires a valid JWT token (Bearer <token>) in the Swagger UI Authorize dialog (BearerAuth).",
    response_description="Confirmation of record deletion."
)
def delete_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_record = db.query(Record).filter(Record.id == record_id, Record.user_id == current_user.id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if db_record.screenshot_path:
        file_path = db_record.screenshot_path.lstrip("/uploads/")
        full_path = os.path.join("uploads", file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
    db.delete(db_record)
    db.commit()
    return {"detail": "Record deleted"}


@router.put(
    "/{record_id}",
    summary="Update DSL content of a record",
    description="Update the DSL content of a record by its ID. The record must belong to the authenticated user. DSL will be compiled to HTML and CSS. Requires a valid JWT token (Bearer <token>).",
    response_model=RecordResponse,
    response_description="The updated record object with compiled HTML and CSS."
)
def update_record_dsl(
        record_id: int,
        dsl_content: str = Body(..., embed=True),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_record = db.query(Record).filter(
        Record.id == record_id, Record.user_id == current_user.id
    ).first()

    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    if not dsl_content.strip():
        raise HTTPException(status_code=400, detail="dsl_content must not be empty")

    html, css = compile_dsl(dsl_content)
    dsl_content = lint_dsl(dsl_content)
    db_record.created_at = datetime.utcnow()
    db_record.dsl_content = dsl_content
    db.commit()
    db.refresh(db_record)

    return JSONResponse(content={
        "record": {
            "id": db_record.id,
            "screenshot_path": db_record.screenshot_path,
            "dsl_content": db_record.dsl_content,
            "user_id": db_record.user_id,
            "project_id": db_record.project_id,
            "created_at": db_record.created_at.isoformat()
        },
        "compiled_html": html,
        "compiled_css": css
    })


@router.get(
    "/{record_id}",
    response_model=RecordResponse,
    summary="Get a record by ID",
    description="Retrieve a specific record by its ID, only if it belongs to the authenticated user. Compiles DSL to HTML and CSS.",
    response_description="The record object with compiled HTML and CSS."
)
def get_record_by_id(
        record_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_record = db.query(Record).filter(
        Record.id == record_id, Record.user_id == current_user.id
    ).first()

    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    html, css = compile_dsl(db_record.dsl_content) if db_record.dsl_content else (None, None)

    return JSONResponse(content={
        "record": {
            "id": db_record.id,
            "screenshot_path": db_record.screenshot_path,
            "dsl_content": db_record.dsl_content,
            "user_id": db_record.user_id,
            "project_id": db_record.project_id,
            "created_at": db_record.created_at.isoformat()
        },
        "compiled_html": html,
        "compiled_css": css
    })
