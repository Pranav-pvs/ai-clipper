from fastapi import APIRouter, HTTPException

from app.schemas.project import ALLOWED_CATEGORIES, Project, ProjectCreate
from app.services import project_store

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=Project, status_code=201)
def create_project(data: ProjectCreate) -> Project:
    if data.category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=422, detail="Unknown content category.")
    return project_store.create_project(data)


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str) -> Project:
    project = project_store.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project