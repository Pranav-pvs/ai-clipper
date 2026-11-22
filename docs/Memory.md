# AI Clipper — Session Memory & Progress Log

Purpose: lets work resume across sessions and across AI tools (Claude, Codex, etc.) without losing context. Update this file at the end of every working session.

## How to use this file
- Add a new dated entry each session summarizing what was done.
- Always record: current phase, what's done, what's in progress, what's blocked, and the next step.
- Keep entries short — this is a log, not a doc dump.

---

## Current Status
- **Current phase:** Phase 1 — Foundation
- **Status:** Not yet started. Repository has not yet been inspected.
- **Next step:** Inspect repository/Git status, identify existing files and dependencies, present Phase 1 implementation plan, and wait for approval before creating/modifying files.

## Decisions Log
| Date | Decision |
|---|---|
| 2026-11-20 | Backend language confirmed as Python (FastAPI) over Rust — ecosystem fit for Whisper/Gemini, FFmpeg handles heavy lifting regardless of host language. |
| 2026-11-20 | Core project docs created: PRD.md, Architecture.md, Rules.md, Phases.md, Design.md, Memory.md. |

## Session Log

### 2026-11-20
- Created the 6 mandatory project docs (PRD, Architecture, Rules, Phases, Design, Memory) from the master project instructions.
- No code written yet. Repository has not been inspected.
- **Next:** Inspect repo → present Phase 1 plan → get approval → begin Phase 1 implementation in small steps.

---

## Template for New Entries
```
### YYYY-MM-DD
- What was done:
- Files created/modified:
- Tests run / results:
- What remains incomplete:
- Next step:
```

### Phase 2 progress (transcription)
- FFmpeg 9.0.1 installed; audio extraction to 16 kHz mono FLAC verified on real speech.
- Groq API used for transcription (`whisper-large-v3-turbo`), chosen because the laptop (i3-1215U, 8 GB RAM) cannot run Whisper locally. Key stored in `backend/.env`, ignored by Git.
- Uploaded videos saved to `backend/uploads_tmp/` (ignored by Git). Links are in memory and reset on restart.
- Projects and transcripts are stored in memory. Supabase is planned but not yet connected.
- `POST /projects/{id}/transcribe` verified end to end with a 59-second speech clip.
- Tests: 32 backend tests passing.
- Next: Gemini highlight suggestions, or Supabase migration (decision pending).