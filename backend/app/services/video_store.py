from pathlib import Path

# In-memory map of project ID -> saved video path. Cleared on server restart.
_video_paths: dict[str, Path] = {}


def save_video_path(project_id: str, path: Path) -> None:
    _video_paths[project_id] = path


def get_video_path(project_id: str) -> Path | None:
    """Return the saved video path, or None if it is unknown or the file is gone."""
    path = _video_paths.get(project_id)
    if path is None or not path.exists():
        _video_paths.pop(project_id, None)
        return None
    return path


def clear_video_paths() -> None:
    """Used by tests and to reset state."""
    _video_paths.clear()