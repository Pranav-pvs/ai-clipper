import uuid

from app.schemas.project import Project, ProjectCreate, TranscriptSegmentOut
from app.services import database

TABLE = "projects"


def _table():
    return database.get_client().table(TABLE)


def _is_valid_id(project_id: str) -> bool:
    """Postgres rejects non-UUID strings, so check first and treat them as 'not found'."""
    try:
        uuid.UUID(project_id)
        return True
    except ValueError:
        return False


def _to_project(row: dict) -> Project:
    data = {key: row.get(key) for key in Project.model_fields}
    data["transcript_segments"] = data["transcript_segments"] or []
    return Project.model_validate(data)


def create_project(data: ProjectCreate) -> Project:
    row = {
        "id": str(uuid.uuid4()),
        **data.model_dump(),
        "transcript_text": None,
        "transcript_segments": [],
    }
    _table().insert(row).execute()
    return _to_project(row)


def get_project(project_id: str) -> Project | None:
    if not _is_valid_id(project_id):
        return None
    result = _table().select("*").eq("id", project_id).execute()
    if not result.data:
        return None
    return _to_project(result.data[0])


def _update(project_id: str, changes: dict) -> Project | None:
    if not _is_valid_id(project_id):
        return None
    result = _table().update(changes).eq("id", project_id).execute()
    if not result.data:
        return None
    return _to_project(result.data[0])


def update_video_metadata(project_id: str, filename: str, size_bytes: int) -> Project | None:
    return _update(project_id, {"video_filename": filename, "video_size_bytes": size_bytes})


def update_transcript(
    project_id: str, text: str, segments: list[TranscriptSegmentOut]
) -> Project | None:
    # Convert to plain dicts: the Supabase client can only send JSON-compatible values
    return _update(
        project_id,
        {
            "transcript_text": text,
            "transcript_segments": [s.model_dump() for s in segments],
        },
    )


def clear_projects() -> None:
    """Tests only. Deletes every row, so never call this from application code."""
    _table().delete().execute()