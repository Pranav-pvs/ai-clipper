import os
from dataclasses import dataclass, field
from pathlib import Path

from groq import Groq

TRANSCRIPTION_MODEL = "whisper-large-v3-turbo"


class TranscriptionError(Exception):
    """Raised when transcription cannot be completed."""


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass
class Transcript:
    text: str
    duration: float
    segments: list[TranscriptSegment] = field(default_factory=list)


def transcribe_audio(audio_path: Path, client: Groq | None = None) -> Transcript:
    """Send an audio file to Groq and return the transcript with timestamps."""
    if not audio_path.exists():
        raise TranscriptionError(f"Audio file not found: {audio_path.name}")

    if client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise TranscriptionError("GROQ_API_KEY is not set.")
        client = Groq(api_key=api_key)

    try:
        with audio_path.open("rb") as audio_file:
            response = client.audio.transcriptions.create(
                file=(audio_path.name, audio_file.read()),
                model=TRANSCRIPTION_MODEL,
                response_format="verbose_json",
            )
    except Exception as exc:
        raise TranscriptionError(f"Groq transcription failed: {exc}") from exc

    segments = [
        TranscriptSegment(start=s["start"], end=s["end"], text=s["text"].strip())
        for s in (getattr(response, "segments", None) or [])
    ]
    return Transcript(
        text=response.text.strip(),
        duration=float(getattr(response, "duration", 0.0) or 0.0),
        segments=segments,
    )