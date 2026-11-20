# AI Clipper — Development Phases

Build in order. Do not skip phases or implement future-phase functionality early.
Each phase must meet its completion requirements before moving to the next — see `Rules.md` §9.

## Phase 1 — Foundation
**Goal:** Basic functional application (no AI yet).
- Inspect repo, create project structure
- Configure Next.js + TypeScript + Tailwind
- Build responsive dashboard, navigation/sidebar
- Build "New Project" workflow + category selection
- Implement video upload UI
- Configure FastAPI, backend health endpoint, basic video validation
- Connect frontend ↔ backend, add error handling
- Initial tests, README/docs updated, commit to GitHub

**Done when:** dashboard works, project creation works, uploads work, backend validates files, project info retrievable, frontend/backend communicate, tests pass.

## Phase 2 — AI Transcription & Analysis
- Extract audio, transcribe speech, store transcript + timestamps
- Analyze transcript via Gemini (category-aware)
- Identify highlights, generate clip suggestions
- Apply custom duration constraints, rank clips, remove duplicates

## Phase 3 — Automatic Clip Generation
- Generate clips with FFmpeg from selected timestamps
- Handle audio/video sync, validate output
- Save and display generated clips in dashboard
- Handle processing failures gracefully

## Phase 4 — Caption & Music Studio
- Generate subtitles, build caption presets (gaming/podcast/sports) + customization + animation
- Implement licensed music library, automatic recommendations, audio mixing

## Phase 5 — Video Editing Studio
- Video preview + editing timeline
- Smart vertical cropping, face/speaker tracking, zoom effects
- Manual adjustments, preview functionality

## Phase 6 — Final Export
- 1080p export, 9:16 presets, final MP4 generation
- Export progress, file validation, download functionality, export history

## Phase 7 — Advanced Features
- Category-specific AI prompts/models (better gaming/sports detection)
- Better speaker detection, batch processing, advanced clip scoring
- YouTube/Instagram integrations (only via official APIs + permissions)

---
**Current phase:** Phase 1 — Foundation (not yet started — awaiting repo inspection & plan approval)
