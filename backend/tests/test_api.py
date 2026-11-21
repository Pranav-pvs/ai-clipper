from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_mp4_is_accepted():
    response = client.post(
        "/projects/validate-upload",
        files={"file": ("clip.mp4", b"fake video bytes", "video/mp4")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["filename"] == "clip.mp4"
    assert body["size_bytes"] == len(b"fake video bytes")


def test_text_file_is_rejected_by_extension():
    response = client.post(
        "/projects/validate-upload",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is False
    assert "extension" in body["reason"]


def test_empty_file_is_rejected():
    response = client.post(
        "/projects/validate-upload",
        files={"file": ("empty.mp4", b"", "video/mp4")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is False
    assert body["reason"] == "File is empty."


def test_wrong_content_type_is_rejected():
    response = client.post(
        "/projects/validate-upload",
        files={"file": ("clip.mp4", b"fake video bytes", "text/plain")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is False
    assert body["reason"] == "Unsupported content type."