from pathlib import Path

from fastapi import UploadFile

from app.core import config


class VideoStorageError(Exception):
    """Raised when an uploaded video cannot be stored."""

    def __init__(self, message: str, status_code: int = 422):
        super().__init__(message)
        self.status_code = status_code


async def save_video(file: UploadFile, project_id: str) -> Path:
    """Save the upload as UPLOAD_DIR/<project_id><extension> and return the path."""
    config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename or "").suffix.lower()
    destination = config.UPLOAD_DIR / f"{project_id}{extension}"
    total_bytes = 0

    try:
        with destination.open("wb") as output:
            while chunk := await file.read(config.CHUNK_SIZE):
                total_bytes += len(chunk)
                if total_bytes > config.MAX_FILE_SIZE_BYTES:
                    raise VideoStorageError(
                        "File is too large. The maximum size is 2 GB.", status_code=413
                    )
                output.write(chunk)

        if total_bytes == 0:
            raise VideoStorageError("File is empty.")
    except Exception:
        # Never leave a partial or invalid file behind
        destination.unlink(missing_ok=True)
        raise

    return destination