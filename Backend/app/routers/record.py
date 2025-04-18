from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from Backend.app.models.record import Record
from Backend.app.schemas.record import RecordImageCreate, RecordDslCreate, RecordResponse
from Backend.app.dependencies.auth import get_current_user
from Backend.app.config.database import get_db
from Backend.app.models.user import User
import os
from datetime import datetime
from Backend.app.services.dsl_service import compile_dsl

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

    # Create record
    # todo: dsl_content for the image with model
    db_record = Record(
        screenshot_path=screenshot_url,
        dsl_content="row { box , box }",
        user_id=current_user.id,
        project_id=project_id,
        created_at=datetime.utcnow()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


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
    htmlCode = compile_dsl(dsl_content, "web")
    return {
        "recordId": db_record.id,
        "Html": htmlCode,
        "css": "css"
    }


@router.get(
    "/{record_id}",
    response_model=RecordResponse,
    summary="Get record by ID",
    description="Retrieve a record's details by its ID, belonging to the authenticated user. If the record has a screenshot, screenshot_path is a URL (e.g., /uploads/<filename>). Requires a valid JWT token (Bearer <token>) in the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The record object."
)
def read_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_record = db.query(Record).filter(Record.id == record_id, Record.user_id == current_user.id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return {
        "screenshotPath": db_record.screenshot_path,
        "dsl_code": db_record.dsl_content,
        "Html": compile_dsl(db_record.dsl_content, "web"),
        "Css ": "css"
    }


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
