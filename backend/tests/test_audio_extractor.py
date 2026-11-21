from pathlib import Path
import subprocess

import pytest

from app.services import audio_extractor
from app.services.audio_extractor import AudioExtractionError, extract_audio


def test_raises_when_ffmpeg_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(audio_extractor.shutil, "which", lambda _name: None)

    with pytest.raises(AudioExtractionError, match="not installed"):
        extract_audio(Path("clip.mp4"), tmp_path)


def test_returns_flac_path_when_ffmpeg_succeeds(monkeypatch, tmp_path):
    monkeypatch.setattr(audio_extractor.shutil, "which", lambda _name: "ffmpeg")

    def fake_run(command, **kwargs):
        # Simulate FFmpeg writing the output file
        Path(command[-1]).write_bytes(b"fake flac")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(audio_extractor.subprocess, "run", fake_run)

    output = extract_audio(Path("clip.mp4"), tmp_path)

    assert output == tmp_path / "clip_audio.flac"
    assert output.exists()


def test_command_uses_mono_16khz_flac(monkeypatch, tmp_path):
    monkeypatch.setattr(audio_extractor.shutil, "which", lambda _name: "ffmpeg")
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        Path(command[-1]).write_bytes(b"fake flac")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(audio_extractor.subprocess, "run", fake_run)

    extract_audio(Path("clip.mp4"), tmp_path)

    command = captured["command"]
    assert "-vn" in command
    assert command[command.index("-ac") + 1] == "1"
    assert command[command.index("-ar") + 1] == "16000"
    assert command[command.index("-c:a") + 1] == "flac"


def test_raises_when_ffmpeg_fails(monkeypatch, tmp_path):
    monkeypatch.setattr(audio_extractor.shutil, "which", lambda _name: "ffmpeg")

    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="No audio stream")

    monkeypatch.setattr(audio_extractor.subprocess, "run", fake_run)

    with pytest.raises(AudioExtractionError, match="No audio stream"):
        extract_audio(Path("clip.mp4"), tmp_path)