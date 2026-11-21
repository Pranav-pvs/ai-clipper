from fastapi import APIRouter, File, UploadFile

router = APIRouter(prefix="/projects", tags=["projects"])

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm"}
ALLOWED_CONTENT_TYPES = {"video/mp4", "video/quicktime", "video/webm"}
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024 * 1024  # 2 GB
CHUNK_SIZE = 1024 * 1024  # read 1 MB at a time


@router.post("/validate-upload")
async def validate_upload(file: UploadFile = File(...)) -> dict:
    """Check an uploaded video without saving it."""
    filename = file.filename or ""
    extension = ""
    if "." in filename:
        extension = "." + filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return {"valid": False, "reason": "Unsupported file extension. Use MP4, MOV, or WebM."}

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return {"valid": False, "reason": "Unsupported content type."}

    # Count bytes in chunks so a huge file never sits fully in memory
    total_bytes = 0
    while chunk := await file.read(CHUNK_SIZE):
        total_bytes += len(chunk)
        if total_bytes > MAX_FILE_SIZE_BYTES:
            return {"valid": False, "reason": "File is too large. The maximum size is 2 GB."}

    if total_bytes == 0:
        return {"valid": False, "reason": "File is empty."}

    return {
        "valid": True,
        "filename": filename,
        "size_bytes": total_bytes,
    }