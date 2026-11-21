from fastapi import APIRouter, File, UploadFile

from app.core import config

router = APIRouter(prefix="/projects", tags=["projects"])

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm"}
ALLOWED_CONTENT_TYPES = {"video/mp4", "video/quicktime", "video/webm"}


def check_video_type(filename: str, content_type: str | None) -> str | None:
    """Return a rejection reason, or None if the file type is allowed."""
    extension = ""
    if "." in filename:
        extension = "." + filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return "Unsupported file extension. Use MP4, MOV, or WebM."

    if content_type not in ALLOWED_CONTENT_TYPES:
        return "Unsupported content type."

    return None


@router.post("/validate-upload")
async def validate_upload(file: UploadFile = File(...)) -> dict:
    """Check an uploaded video without saving it."""
    filename = file.filename or ""

    reason = check_video_type(filename, file.content_type)
    if reason:
        return {"valid": False, "reason": reason}

    # Count bytes in chunks so a huge file never sits fully in memory
    total_bytes = 0
    while chunk := await file.read(config.CHUNK_SIZE):
        total_bytes += len(chunk)
        if total_bytes > config.MAX_FILE_SIZE_BYTES:
            return {"valid": False, "reason": "File is too large. The maximum size is 2 GB."}

    if total_bytes == 0:
        return {"valid": False, "reason": "File is empty."}

    return {
        "valid": True,
        "filename": filename,
        "size_bytes": total_bytes,
    }