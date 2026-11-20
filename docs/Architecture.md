# AI Clipper — Architecture

## 1. Language/Stack Decision: Python vs Rust
**Decision: Python (FastAPI) for the backend.**

Reasoning:
- Whisper (speech-to-text), the Gemini SDK, and most AI/video-adjacent tooling are
  Python-first — using Python avoids fighting the ecosystem.
- FFmpeg does the actual video/audio processing as an external subprocess regardless of
  which backend language calls it — so Rust wouldn't speed up encoding/transcoding itself.
- Rust's advantage (raw performance, memory safety) matters most for a narrow, *measured*
  bottleneck — e.g., a custom frame-analysis loop — not for an API/orchestration layer.
- Revisit only if profiling later shows a specific CPU-bound step in the Python layer
  (not FFmpeg itself) is the bottleneck. Don't introduce a second language preemptively.

## 2. Monorepo Layout
```
ai-clipper/
│
├── frontend/                 # Next.js + React + TypeScript + Tailwind
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   │   ├── dashboard/
│   │   │   ├── projects/
│   │   │   ├── editor/
│   │   │   ├── settings/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── dashboard/
│   │   │   ├── upload/
│   │   │   └── navigation/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── services/
│   │   └── types/
│   └── package.json
│
├── backend/                  # Python + FastAPI
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── processors/       # FFmpeg, Whisper, Gemini orchestration
│   │   ├── workers/          # Celery background jobs
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── shared/types/              # Shared TS/schema types
├── docs/                      # PRD, Architecture, Phases, Design, Rules, Memory
├── .gitignore
└── README.md
```
Structural changes must be explained before being made — see `Rules.md`.

## 3. System Components
| Layer | Technology | Role |
|---|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind | Dashboard, project workflow, editor UI |
| Backend API | Python, FastAPI | Business logic, orchestration, REST endpoints |
| Video processing | FFmpeg (subprocess) | Trimming, cropping, encoding, format conversion |
| Speech-to-text | Whisper or equivalent API | Transcription + timestamps |
| AI analysis | Gemini API (modular provider layer) | Highlight detection, scoring, reasoning |
| Database | PostgreSQL via Supabase | Projects, clips, users, metadata |
| Auth | Supabase Auth | Introduced when auth is needed |
| File storage | Cloudflare R2 | Uploaded videos, generated clips, assets |
| Background jobs | Redis + Celery | Long-running processing (introduced when needed) |

Infrastructure (auth, Redis/Celery, etc.) is added only when the current phase requires it —
not all at once (see `Rules.md` §Dependencies).

## 4. Data Flow (high level)
1. User uploads video / provides authorized URL → stored in R2, metadata in Postgres.
2. Backend extracts audio → transcribes via Whisper → stores transcript + timestamps.
3. Transcript sent to Gemini (category-aware prompt) → returns ranked highlight candidates.
4. FFmpeg cuts clips per approved timestamps → stores clip files.
5. Caption/music studio applies styling and audio mixing to a clip.
6. Export pipeline renders final 1080×1920 MP4 → validates output → makes available for download.

## 5. AI Provider Modularity
The AI analysis layer must be provider-agnostic: Gemini is the initial provider, but the
interface should allow swapping/adding models later without rewriting calling code.

## 6. Related Documents
See `PRD.md` for product scope, `Rules.md` for engineering constraints, `Phases.md` for
build order.
