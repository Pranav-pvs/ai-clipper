from fastapi.testclient import TestClient

from app.core import config
from app.main import app
from app.services import project_store, video_store

client = TestClient(app)
VIDEO_BYTES = b"fake video bytes"


import pytest


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    """Send uploads to a temporary folder and reset the in-memory stores."""
    monkeypatch.setattr(config, "UPLOAD_DIR", tmp_path / "uploads")
    project_store.clear_projects()
    video_store.clear_video_paths()
    yield
    project_store.clear_projects()
    video_store.clear_video_paths()


def create_project() -> dict:
    return client.post("/projects", json={"name": "Clip", "category": "Gaming"}).json()


def upload(project_id: str, filename: str = "clip.mp4", content_type: str = "video/mp4"):
    return client.post(
        f"/projects/{project_id}/video",
        files={"file": (filename, VIDEO_BYTES, content_type)},
    )


def test_upload_saves_file_and_updates_project():
    project = create_project()

    response = upload(project["id"])

    assert response.status_code == 201
    body = response.json()
    assert body["video_filename"] == "clip.mp4"
    assert body["video_size_bytes"] == len(VIDEO_BYTES)
    assert "video_path" not in body  # local paths are never exposed

    saved = video_store.get_video_path(project["id"])
    assert saved is not None
    assert saved.read_bytes() == VIDEO_BYTES


def test_upload_to_unknown_project_returns_404():
    response = upload("does-not-exist")
    assert response.status_code == 404


def test_invalid_type_is_rejected_and_not_saved():
    project = create_project()

    response = upload(project["id"], filename="notes.txt", content_type="text/plain")

    assert response.status_code == 422
    assert video_store.get_video_path(project["id"]) is None
    assert not config.UPLOAD_DIR.exists() or not any(config.UPLOAD_DIR.iterdir())


def test_oversized_file_is_rejected(monkeypatch):
    monkeypatch.setattr(config, "MAX_FILE_SIZE_BYTES", 5)
    project = create_project()

    response = upload(project["id"])

    assert response.status_code == 413
    assert video_store.get_video_path(project["id"]) is None


def test_deleted_file_is_handled_gracefully():
    project = create_project()
    upload(project["id"])
    video_store.get_video_path(project["id"]).unlink()

    assert video_store.get_video_path(project["id"]) is None


def test_restart_clears_video_links_without_crashing():
    project = create_project()
    upload(project["id"])
    saved = video_store.get_video_path(project["id"])

    # Simulate a server restart: in-memory stores are empty, but the file stays on disk
    project_store.clear_projects()
    video_store.clear_video_paths()

    assert saved.exists()
    assert video_store.get_video_path(project["id"]) is None
    assert client.get(f"/projects/{project['id']}").status_code == 404