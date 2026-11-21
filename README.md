# AI Clipper

**Create More. Edit Less.**

AI Clipper is an AI-powered web platform that turns long-form videos into short, engaging clips for YouTube Shorts, Instagram Reels, and TikTok.

> Status: Phase 1 (Foundation) — dashboard, project form, upload validation, and tests. AI analysis, clip generation, captions, music, and export are planned for later phases. See `docs/Phases.md`.

## Project structure

```
AI-Clipper/
├── backend/      # Python + FastAPI API
├── frontend/     # Next.js + React + TypeScript + Tailwind
├── docs/         # Product, architecture, rules, phases, design, progress log
└── README.md
```

## Requirements

- Git
- Node.js 18.18 or newer (LTS recommended)
- Python 3.11 or newer (3.12 is the most widely tested)

## Run the backend

From the repo root:

```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.
- Health check: `http://127.0.0.1:8000/health`
- API docs: `http://127.0.0.1:8000/docs`

## Run the frontend

In a second terminal, from the repo root:

```
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. Start the backend first so the New Project form can check uploads.

## Run the tests

Backend tests (with the venv active, from `backend/`):

```
pip install -r requirements-dev.txt
python -m pytest -v
```

Frontend lint (from `frontend/`):

```
npm run lint
```

## Permissions and content

AI Clipper is only meant for videos you own or have permission to edit. It does not download videos from URLs or bypass platform restrictions. Use only licensed music. See `docs/Rules.md`.