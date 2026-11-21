from fastapi import APIRouter, File, HTTPException, UploadFile

from app.routes.uploads import check_video_type
from app.schemas.project import ALLOWED_CATEGORIES, Project, ProjectCreate
from app.services import project_store, video_store
from app.services.video_storage import VideoStorageError, save_video

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


@router.post("/{project_id}/video", response_model=Project, status_code=201)
async def upload_project_video(project_id: str, file: UploadFile = File(...)) -> Project:
    if project_store.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found.")

    reason = check_video_type(file.filename or "", file.content_type)
    if reason:
        raise HTTPException(status_code=422, detail=reason)

    try:
        path = await save_video(file, project_id)
    except VideoStorageError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc

    # Replacing an earlier upload: remove the old file if it has a different name
    previous = video_store.get_video_path(project_id)
    if previous is not None and previous != path:
        previous.unlink(missing_ok=True)

    video_store.save_video_path(project_id, path)
    updated = project_store.update_video_metadata(
        project_id, file.filename or path.name, path.stat().st_size
    )
    return updated