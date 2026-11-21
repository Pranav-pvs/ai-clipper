import uuid

from app.schemas.project import Project, ProjectCreate

# In-memory storage. Data resets when the server restarts.
# Replaced by Supabase in Phase 2.
_projects: dict[str, Project] = {}


def create_project(data: ProjectCreate) -> Project:
    project = Project(id=str(uuid.uuid4()), **data.model_dump())
    _projects[project.id] = project
    return project


def get_project(project_id: str) -> Project | None:
    return _projects.get(project_id)


def clear_projects() -> None:
    """Used by tests to reset state."""
    _projects.clear()