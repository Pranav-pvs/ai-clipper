from pathlib import Path
from types import SimpleNamespace

import pytest

from app.services.transcription import TranscriptionError, transcribe_audio


class FakeTranscriptions:
    def __init__(self, response=None, error=None):
        self._response = response
        self._error = error
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self._error:
            raise self._error
        return self._response


class FakeClient:
    def __init__(self, transcriptions):
        self.audio = SimpleNamespace(transcriptions=transcriptions)


def make_audio(tmp_path: Path) -> Path:
    path = tmp_path / "clip_audio.flac"
    path.write_bytes(b"fake flac")
    return path


def test_returns_text_duration_and_segments(tmp_path):
    response = SimpleNamespace(
        text=" Hello world ",
        duration=2.5,
        segments=[{"start": 0.0, "end": 1.2, "text": " Hello"}, {"start": 1.2, "end": 2.5, "text": " world "}],
    )
    fake = FakeTranscriptions(response=response)

    result = transcribe_audio(make_audio(tmp_path), client=FakeClient(fake))

    assert result.text == "Hello world"
    assert result.duration == 2.5
    assert [s.text for s in result.segments] == ["Hello", "world"]
    assert fake.calls[0]["model"] == "whisper-large-v3-turbo"


def test_missing_file_raises(tmp_path):
    with pytest.raises(TranscriptionError, match="not found"):
        transcribe_audio(tmp_path / "missing.flac", client=FakeClient(FakeTranscriptions()))


def test_api_error_is_wrapped(tmp_path):
    fake = FakeTranscriptions(error=RuntimeError("401 Invalid API Key"))

    with pytest.raises(TranscriptionError, match="401"):
        transcribe_audio(make_audio(tmp_path), client=FakeClient(fake))


def test_missing_api_key_raises(tmp_path, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with pytest.raises(TranscriptionError, match="GROQ_API_KEY"):
        transcribe_audio(make_audio(tmp_path))