from typing import List, Optional

from pydantic import BaseModel

from Compiler_V2 import compile_dsl_safe, lint_dsl
from app.models.project import Project
from app.models.record import Record
from app.schemas.record import RecordItem


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(BaseModel):
    id: int
    name: str
    user_id: int

    @classmethod
    def from_project(cls, project: Project):
        return cls(
            user_id=project.user_id,
            name=project.name,
            id=project.id
        )


class ProjectWithRecordsResponse(BaseModel):
    project: ProjectResponse
    records: List[RecordItem]


class GetFullProject(BaseModel):
    id: int
    name: str
    user_id: int
    records: List[RecordItem]

    @classmethod
    def from_project(cls, proj: Project, records: list[Record]):
        record_items = [
            RecordItem(
                record_id=record.id,
                screenshot_path=record.screenshot_path,
                dsl=lint_dsl(record.dsl_content),
                html=compile_dsl_safe(record.dsl_content)[0],
                css=compile_dsl_safe(record.dsl_content)[1],
                createdAt=record.created_at
            )
            for record in records
        ]
        return cls(
            id=proj.id,
            name=proj.name,
            user_id=proj.user_id,
            records=record_items
        )


class UpdateProject(BaseModel):
    name: Optional[str]


class GetAllProjectsResponse(BaseModel):
    numberOfProjects: int
    projects: List[ProjectResponse]
