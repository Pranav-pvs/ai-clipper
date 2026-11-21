import uuid

from app.schemas.project import Project, ProjectCreate, TranscriptSegmentOut

# In-memory storage. Data resets when the server restarts.
# Replaced by Supabase in Phase 2.
_projects: dict[str, Project] = {}


def create_project(data: ProjectCreate) -> Project:
    project = Project(id=str(uuid.uuid4()), **data.model_dump())
    _projects[project.id] = project
    return project


def get_project(project_id: str) -> Project | None:
    return _projects.get(project_id)


def update_video_metadata(project_id: str, filename: str, size_bytes: int) -> Project | None:
    project = _projects.get(project_id)
    if project is None:
        return None
    updated = project.model_copy(
        update={"video_filename": filename, "video_size_bytes": size_bytes}
    )
    _projects[project_id] = updated
    return updated


def update_transcript(
    project_id: str, text: str, segments: list[TranscriptSegmentOut]
) -> Project | None:
    project = _projects.get(project_id)
    if project is None:
        return None
    updated = project.model_copy(
        update={"transcript_text": text, "transcript_segments": segments}
    )
    _projects[project_id] = updated
    return updated


def clear_projects() -> None:
    """Used by tests to reset state."""
    _projects.clear()