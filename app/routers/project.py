from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, UpdateProject, GetAllProjectsResponse, GetFullProject
from app.services.ProjectService import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ProjectService(db, current_user)


@router.post("/", response_model=ProjectResponse)
def create_project(
        project: ProjectCreate,
        service: ProjectService = Depends(get_project_service)
):
    return service.add_new_project(project)


@router.get("/{project_id}", response_model=GetFullProject)
def read_project(
        project_id: int,
        service: ProjectService = Depends(get_project_service)
):
    return service.get_project(project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
        project_id: int,
        project: UpdateProject,
        service: ProjectService = Depends(get_project_service)
):
    return service.update_project(project_id, project)


@router.delete("/{project_id}")
def delete_project(
        project_id: int,
        service: ProjectService = Depends(get_project_service)
):
    return service.delete_project_service(project_id)


@router.get("/", response_model=GetAllProjectsResponse)
def get_all_projects(
        service: ProjectService = Depends(get_project_service)
):
    return service.get_all_projects()
