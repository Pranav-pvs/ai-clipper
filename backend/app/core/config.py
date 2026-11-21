from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]

# Load backend/.env so GROQ_API_KEY is available. Existing environment variables win.
load_dotenv(BACKEND_DIR / ".env")

UPLOAD_DIR = BACKEND_DIR / "uploads_tmp"
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024 * 1024  # 2 GB upload limit
CHUNK_SIZE = 1024 * 1024  # read 1 MB at a time

# Groq rejects large audio files. Keep this under its documented limit.
GROQ_MAX_AUDIO_BYTES = 25 * 1024 * 1024  # 25 MB