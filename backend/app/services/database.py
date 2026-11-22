from functools import lru_cache

from supabase import Client, create_client

from app.core import config


class DatabaseNotConfiguredError(Exception):
    """Raised when Supabase settings are missing from backend/.env."""


@lru_cache(maxsize=1)
def get_client() -> Client:
    """Create the Supabase client once and reuse it. Uses the service key (backend only)."""
    if not config.SUPABASE_URL or not config.SUPABASE_SERVICE_KEY:
        raise DatabaseNotConfiguredError(
            "Supabase is not configured. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in backend/.env."
        )
    return create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)