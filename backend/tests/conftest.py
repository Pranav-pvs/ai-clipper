import pytest

from app.services import database
from tests.fake_supabase import FakeSupabase


@pytest.fixture(autouse=True)
def fake_database(monkeypatch):
    """Every test uses an in-memory fake, so tests never touch the real Supabase project."""
    fake = FakeSupabase()
    monkeypatch.setattr(database, "get_client", lambda: fake)
    yield fake