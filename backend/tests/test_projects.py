from fastapi.testclient import TestClient

from app.main import app
from app.services import project_store

client = TestClient(app)


def setup_function():
    project_store.clear_projects()


def test_create_project_returns_id():
    response = client.post(
        "/projects",
        json={"name": "Weekly highlights", "category": "Gaming", "video_filename": "a.mp4", "video_size_bytes": 100},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["name"] == "Weekly highlights"
    assert body["category"] == "Gaming"


def test_get_project_returns_created_project():
    created = client.post("/projects", json={"name": "Pod", "category": "Podcasts"}).json()
    response = client.get(f"/projects/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_unknown_project_returns_404():
    response = client.get("/projects/does-not-exist")
    assert response.status_code == 404


def test_empty_name_is_rejected():
    response = client.post("/projects", json={"name": "", "category": "Gaming"})
    assert response.status_code == 422


def test_unknown_category_is_rejected():
    response = client.post("/projects", json={"name": "Test", "category": "Movies"})
    assert response.status_code == 422