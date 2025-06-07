from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from Compiler_V2 import compile_dsl, lint_dsl
from app.models.record import Record


class RecordItem(BaseModel):
    record_id: int
    screenshot_path: Optional[str]
    dsl: Optional[str]
    html: Optional[str]
    css: Optional[str]
    createdAt: datetime


class RecordResponse(BaseModel):
    record: dict  # Keep as dict to match JSONResponse structure
    compiled_html: Optional[str]
    compiled_css: Optional[str]


class GetRecordResponse(BaseModel):
    record_id: int
    project_id: Optional[int]
    screenshot_path: Optional[str]
    dsl: str
    html: str
    css: str
    createdAt: datetime

    #
    # @classmethod
    # def from_anonymous(cls, dsl, html, css):
    #     return cls(
    #         css=css,
    #         html=html,
    #         dsl=dsl,
    #         createdAt=datetime.utcnow()
    #     )

    @classmethod
    def from_record(cls, record: Record):
        html, css = compile_dsl(record.dsl_content)
        dsl = lint_dsl(record.dsl_content)
        return cls(
            record_id=record.id,
            project_id=record.project_id,
            screenshot_path=record.screenshot_path,
            dsl=dsl,
            html=html,
            css=css,
            createdAt=record.created_at
        )


class GetAllRecordResponse(BaseModel):
    numberOfRecords: int
    records: list[GetRecordResponse]


class UpdateRecord(BaseModel):
    dsl_content: Optional[str]
