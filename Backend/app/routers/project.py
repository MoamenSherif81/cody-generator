from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.app.models.project import Project
from Backend.app.schemas.project import ProjectCreate, ProjectResponse
from Backend.app.dependencies.auth import get_current_user
from Backend.app.config.database import get_db
from Backend.app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=ProjectResponse,
    summary="Create a new project",
    description="Create a project for the authenticated user. Requires a valid JWT token in the Authorization header (Bearer <token>), entered via the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The created project object."
)
def create_project(project: ProjectCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_project = Project(name=project.name, user_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
    description="Retrieve a project's details by its ID. Requires a valid JWT token in the Authorization header (Bearer <token>), entered via the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The project object."
)
def read_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.delete(
    "/{project_id}",
    summary="Delete a project",
    description="Delete a project by its ID. Requires a valid JWT token in the Authorization header (Bearer <token>), entered via the Swagger UI Authorize dialog (BearerAuth).",
    response_description="Confirmation of project deletion."
)
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"detail": "Project deleted"}


@router.get(
    "/",
    response_model=list[ProjectResponse],
    summary="Get all projects for the current user",
    description="Retrieve all projects owned by the authenticated user. Requires a valid JWT token in the Authorization header (Bearer <token>), entered via the Swagger UI Authorize dialog (BearerAuth).",
    response_description="List of project objects."
)
def get_all_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    return projects
