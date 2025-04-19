from typing import Optional, List

from pydantic import BaseModel


class RecordItem(BaseModel):
    record_id: int
    screenshot_path: Optional[str]  # Allow None for DSL-based records
    dsl_code: Optional[str]
    html: Optional[str]
    css: Optional[str]


class RecordListResponse(BaseModel):
    data: List[RecordItem]


class RecordResponse(BaseModel):
    record: dict  # Keep as dict to match JSONResponse structure
    compiled_html: Optional[str]
    compiled_css: Optional[str]
