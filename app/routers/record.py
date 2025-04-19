import os
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest

from Compiler_V2 import lint_dsl, compile_dsl
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.record import Record, RecordListResponse
from app.models.user import User
from app.schemas.record import RecordResponse
from app.services.ai_service import process_screenshots

router = APIRouter(prefix="/records", tags=["Records"])


def serialize_record(record: Record) -> dict:
    """Serialize a Record object to a dictionary."""
    return {
        "id": record.id,
        "screenshot_path": record.screenshot_path,
        "dsl_content": record.dsl_content,
        "user_id": record.user_id,
        "project_id": record.project_id,
        "created_at": record.created_at.isoformat()
    }


def compile_dsl_safe(dsl_content: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """Compile DSL content to HTML and CSS, handling None case."""
    return compile_dsl(dsl_content) if dsl_content else (None, None)

from fastapi import Form

@router.post(
    "/image",
    summary="Create a record with screenshots",
    description="Upload one or more screenshot images to generate DSL, HTML, and CSS. Optionally save to database with project ID and user authentication. Requires a valid JWT token for authenticated requests.",
    response_description="The created record object (if saved) with screenshot_path as a URL, and compiled HTML, CSS, and DSL."
)


async def create_image_record(
        screenshots: List[UploadFile] = File(...),
        project_id: Optional[int] = Form(None),
        db: Session = Depends(get_db),
        current_user: Optional[User] = Depends(get_current_user, use_cache=False)
):
    # Validate
    if not screenshots:
        raise HTTPException(status_code=400, detail="Please upload at least 1 image")

    # Process screenshots to get DSL, HTML, CSS
    dsl, html, css = await process_screenshots(screenshots)

    # If authenticated, save to disk and database
    if current_user:
        # Save first screenshot (or loop for all if needed)
        screenshot = screenshots[0]
        filename = f"{datetime.utcnow().timestamp()}_{screenshot.filename}"
        file_path = os.path.join("uploads", filename)
        os.makedirs("uploads", exist_ok=True)

        # Reset file pointer to start (since process_screenshots consumed it)
        await screenshot.seek(0)
        with open(file_path, "wb") as f:
            f.write(await screenshot.read())

        screenshot_url = f"/uploads/{filename}"

        # Save record to DB
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
            "record": serialize_record(db_record),
            "compiled_html": html,
            "compiled_css": css,
            "dsl": dsl
        })

    # If not authenticated, return DSL, HTML, CSS only
    return JSONResponse(content={
        "html": html,
        "css": css,
        "dsl": dsl
    })
@router.post(
    "/dsl",
    response_model=RecordResponse,
    summary="Create a record with DSL content",
    description="Create a record with mandatory DSL content, associated with the authenticated user. Project ID is optional. Requires a valid JWT token (Bearer <token>).",
    response_description="The created record object."
)
async def create_dsl_record(
        dsl_content: str = Body(...),
        project_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Validate dsl_content
    if not dsl_content.strip():
        raise HTTPException(status_code=400, detail="DSL content must not be empty")

    # Compile and lint DSL
    html, css = compile_dsl(dsl_content)
    dsl_content = lint_dsl(dsl_content)

    # Create and save record
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
        "record": serialize_record(db_record),
        "compiled_html": html,
        "compiled_css": css
    })


@router.get(
    "/all",
    summary="Get all records with no project",
    description="Retrieve all records that have no project_id, belonging to the authenticated user. Ordered ascending by creation date.",
    response_description="A list of record objects including record_id."
)
def get_records_no_project(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    records = (
        db.query(Record)
        .filter(Record.user_id == current_user.id, Record.project_id.is_(None))
        .order_by(Record.created_at.asc())
        .all()
    )

    response_data = []
    for record in records:
        html, css = compile_dsl_safe(record.dsl_content)
        response_data.append({
            "record_id": record.id,
            "screenshot_path": record.screenshot_path,
            "dsl_code": record.dsl_content,
            "html": html,
            "css": css
        })

    return {"data": response_data}


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
    # Query record by ID and user
    db_record = db.query(Record).filter(
        Record.id == record_id, Record.user_id == current_user.id
    ).first()

    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Compile DSL
    html, css = compile_dsl_safe(db_record.dsl_content)

    return JSONResponse(content={
        "record": serialize_record(db_record),  # Includes id
        "compiled_html": html,
        "compiled_css": css
    })


@router.put(
    "/{record_id}",
    response_model=RecordResponse,
    summary="Update DSL content of a record",
    description="Update the DSL content of a record by its ID. The record must belong to the authenticated user. DSL will be compiled to HTML and CSS. Requires a valid JWT token (Bearer <token>).",
    response_description="The updated record object with compiled HTML and CSS."
)
def update_record_dsl(
        record_id: int,
        dsl_content: str = Body(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Query record by ID and user
    db_record = db.query(Record).filter(
        Record.id == record_id, Record.user_id == current_user.id
    ).first()

    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Validate dsl_content
    if not dsl_content.strip():
        raise HTTPException(status_code=400, detail="DSL content must not be empty")

    # Compile and lint DSL
    html, css = compile_dsl(dsl_content)
    dsl_content = lint_dsl(dsl_content)

    # Update record
    db_record.dsl_content = dsl_content
    db_record.created_at = datetime.utcnow()  # Update timestamp
    db.commit()
    db.refresh(db_record)

    return JSONResponse(content={
        "record": serialize_record(db_record),
        "compiled_html": html,
        "compiled_css": css
    })


@router.delete(
    "/{record_id}",
    summary="Delete a record",
    description="Delete a record by its ID, belonging to the authenticated user. If the record has a screenshot, the file is removed from the uploads directory. Requires a valid JWT token (Bearer <token>).",
    response_description="Confirmation of record deletion."
)
def delete_record(
        record_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Query record by ID and user
    db_record = db.query(Record).filter(
        Record.id == record_id, Record.user_id == current_user.id
    ).first()

    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Delete screenshot file if it exists
    if db_record.screenshot_path:
        file_path = db_record.screenshot_path.lstrip("/uploads/")
        full_path = os.path.join("uploads", file_path)
        if os.path.exists(full_path):
            os.remove(full_path)

    # Delete record
    db.delete(db_record)
    db.commit()
    return {"detail": "Record deleted"}
