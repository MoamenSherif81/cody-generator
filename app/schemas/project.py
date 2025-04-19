from pydantic import BaseModel
from typing import Optional, List
from app.schemas.record import RecordItem

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    user_id: int

class ProjectWithRecordsResponse(BaseModel):
    project: ProjectResponse
    records: List[RecordItem]