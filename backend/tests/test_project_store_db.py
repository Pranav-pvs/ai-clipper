import json

from app.schemas.project import ProjectCreate, TranscriptSegmentOut
from app.services import project_store


def test_transcript_is_saved_as_plain_json(fake_database):
    project = project_store.create_project(ProjectCreate(name="Clip", category="Gaming"))

    project_store.update_transcript(
        project.id, "Hello", [TranscriptSegmentOut(start=0.0, end=1.0, text="Hello")]
    )

    row = fake_database.tables["projects"][0]
    json.dumps(row)  # raises if any value is not JSON-compatible
    assert row["transcript_segments"] == [{"start": 0.0, "end": 1.0, "text": "Hello"}]


def test_non_uuid_id_is_not_found(fake_database):
    assert project_store.get_project("does-not-exist") is None