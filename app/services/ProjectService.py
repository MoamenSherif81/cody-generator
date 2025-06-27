from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.record import Record
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, GetFullProject, UpdateProject, GetAllProjectsResponse


class ProjectService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def add_new_project(self, project: ProjectCreate) -> ProjectResponse:
        db_project = Project(name=project.name, user_id=self.current_user.id)
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return ProjectResponse(
            id=db_project.id,
            user_id=self.current_user.id,
            name=db_project.name,
        )

    def _get_project(self, project_id: int):
        db_project = self.db.query(Project).filter(Project.id == project_id,
                                                   Project.user_id == self.current_user.id).first()
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project

    def get_project(self, project_id: int) -> GetFullProject:
        db_project = self._get_project(project_id)
        records = (self.db.query(Record)
                   .filter(Record.project_id == project_id, Record.user_id == self.current_user.id
                           ).all())

        return GetFullProject.from_project(db_project, records)

    def get_all_projects(self) -> GetAllProjectsResponse:
        db_projects = self.db.query(Project).filter(Project.user_id == self.current_user.id).all()
        projects = [ProjectResponse.from_project(proj) for proj in db_projects]
        return GetAllProjectsResponse(
            numberOfProjects=len(projects) if projects else 0,
            projects=projects
        )

    def update_project(self, project_id: int, proj: UpdateProject):
        db_project = self._get_project(project_id)
        if proj.name:
            db_project.name = proj.name
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def delete_project_service(self, project_id: int):
        db_project = self._get_project(project_id)
        self.db.delete(db_project)
        self.db.commit()
        return {"detail": "Project deleted"}

