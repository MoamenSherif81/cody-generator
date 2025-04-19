from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Compiler_V2 import compile_dsl
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.project import Project
from app.models.record import Record
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


def compile_dsl_safe(dsl_content: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    return compile_dsl(dsl_content) if dsl_content else (None, None)


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_project = Project(name=project.name, user_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/{project_id}")
def read_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    records = db.query(Record).filter(Record.project_id == project_id, Record.user_id == current_user.id).all()
    record_items = [
        {
            "record_id": record.id,
            "screenshot_path": record.screenshot_path,
            "dsl_code": record.dsl_content,
            "html": compile_dsl_safe(record.dsl_content)[0],
            "css": compile_dsl_safe(record.dsl_content)[1],
            "createdAt": record.created_at
        }
        for record in records
    ]

    return {
        "project": {"id": db_project.id, "name": db_project.name, "user_id": db_project.user_id},
        "records": record_items
    }


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_project.name = project.name
    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"detail": "Project deleted"}


@router.get("/", response_model=List[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Project).filter(Project.user_id == current_user.id).all()
