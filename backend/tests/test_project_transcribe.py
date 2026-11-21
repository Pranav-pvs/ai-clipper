from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core import config
from app.main import app
from app.routes import projects as projects_routes
from app.services import project_store, video_store
from app.services.audio_extractor import AudioExtractionError
from app.services.transcription import Transcript, TranscriptionError, TranscriptSegment

client = TestClient(app)
audio_paths_seen: list[Path] = []


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    """Use a temporary upload folder and reset in-memory stores for each test."""
    monkeypatch.setattr(config, "UPLOAD_DIR", tmp_path / "uploads")
    audio_paths_seen.clear()
    project_store.clear_projects()
    video_store.clear_video_paths()
    yield
    project_store.clear_projects()
    video_store.clear_video_paths()


def fake_extract(video_path: Path, output_dir: Path) -> Path:
    """Stand-in for FFmpeg: writes a small fake audio file."""
    output = output_dir / "audio.flac"
    output.write_bytes(b"fake flac")
    audio_paths_seen.append(output)
    return output


def fake_transcribe(audio_path: Path) -> Transcript:
    return Transcript(
        text="Hello there",
        duration=2.0,
        segments=[TranscriptSegment(start=0.0, end=2.0, text="Hello there")],
    )


def create_project_with_video() -> str:
    project = client.post("/projects", json={"name": "Clip", "category": "Gaming"}).json()
    client.post(
        f"/projects/{project['id']}/video",
        files={"file": ("clip.mp4", b"fake video bytes", "video/mp4")},
    )
    return project["id"]


@pytest.fixture
def fake_pipeline(monkeypatch):
    monkeypatch.setattr(projects_routes, "extract_audio", fake_extract)
    monkeypatch.setattr(projects_routes, "transcribe_audio", fake_transcribe)


def test_transcribe_stores_transcript(fake_pipeline):
    project_id = create_project_with_video()

    response = client.post(f"/projects/{project_id}/transcribe")

    assert response.status_code == 200
    body = response.json()
    assert body["transcript_text"] == "Hello there"
    assert body["transcript_segments"] == [{"start": 0.0, "end": 2.0, "text": "Hello there"}]

    # The transcript is also returned by GET
    assert client.get(f"/projects/{project_id}").json()["transcript_text"] == "Hello there"


def test_temporary_audio_is_deleted(fake_pipeline):
    project_id = create_project_with_video()

    client.post(f"/projects/{project_id}/transcribe")

    assert len(audio_paths_seen) == 1
    assert not audio_paths_seen[0].exists()


def test_unknown_project_returns_404(fake_pipeline):
    response = client.post("/projects/does-not-exist/transcribe")
    assert response.status_code == 404


def test_project_without_video_returns_409(fake_pipeline):
    project = client.post("/projects", json={"name": "Clip", "category": "Gaming"}).json()

    response = client.post(f"/projects/{project['id']}/transcribe")

    assert response.status_code == 409


def test_missing_video_after_restart_returns_409(fake_pipeline):
    project_id = create_project_with_video()

    # Simulate a restart: the file may still be on disk, but the link is gone
    video_store.clear_video_paths()

    response = client.post(f"/projects/{project_id}/transcribe")
    assert response.status_code == 409


def test_extraction_failure_returns_502(monkeypatch):
    def failing_extract(video_path, output_dir):
        raise AudioExtractionError("FFmpeg failed: No audio stream")

    monkeypatch.setattr(projects_routes, "extract_audio", failing_extract)
    project_id = create_project_with_video()

    response = client.post(f"/projects/{project_id}/transcribe")

    assert response.status_code == 502
    assert "No audio stream" in response.json()["detail"]


def test_transcription_failure_returns_502(monkeypatch):
    def failing_transcribe(audio_path):
        raise TranscriptionError("Groq transcription failed: 401 Invalid API Key")

    monkeypatch.setattr(projects_routes, "extract_audio", fake_extract)
    monkeypatch.setattr(projects_routes, "transcribe_audio", failing_transcribe)
    project_id = create_project_with_video()

    response = client.post(f"/projects/{project_id}/transcribe")

    assert response.status_code == 502
    assert "401" in response.json()["detail"]


def test_audio_too_large_returns_413(monkeypatch, fake_pipeline):
    monkeypatch.setattr(config, "GROQ_MAX_AUDIO_BYTES", 3)  # fake audio is 9 bytes
    project_id = create_project_with_video()

    response = client.post(f"/projects/{project_id}/transcribe")

    assert response.status_code == 413