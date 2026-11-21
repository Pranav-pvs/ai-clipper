import shutil
import subprocess
from pathlib import Path

FFMPEG_TIMEOUT_SECONDS = 300


class AudioExtractionError(Exception):
    """Raised when FFmpeg cannot produce an audio file."""


def extract_audio(video_path: Path, output_dir: Path) -> Path:
    """Extract mono 16 kHz FLAC audio from a video file.

    Speech models expect 16 kHz mono audio, and FLAC is lossless and accepted by Groq.
    The output file is written to output_dir and its path is returned.
    """
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise AudioExtractionError("FFmpeg is not installed or not on PATH.")

    output_path = output_dir / f"{video_path.stem}_audio.flac"
    command = [
        ffmpeg,
        "-y",  # overwrite output if it exists
        "-i", str(video_path),
        "-vn",  # drop video
        "-ac", "1",  # mono
        "-ar", "16000",  # 16 kHz
        "-c:a", "flac",
        str(output_path),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=FFMPEG_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AudioExtractionError("Audio extraction timed out.") from exc

    if result.returncode != 0 or not output_path.exists():
        # Only the end of FFmpeg's log is useful; keep the error short
        raise AudioExtractionError(f"FFmpeg failed: {result.stderr.strip()[-500:]}")

    return output_path