from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecordImageCreate(BaseModel):
    project_id: Optional[int] = None

class RecordDslCreate(BaseModel):
    dsl_content: str
    project_id: Optional[int] = None

class RecordResponse(BaseModel):
    id: int
    screenshot_path: Optional[str] = None  # URL like /uploads/<filename>
    dsl_content: Optional[str] = None
    project_id: Optional[int] = None
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True