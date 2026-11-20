# AI Clipper — Product Requirements Document (PRD)

## 1. Product Name & Tagline
**AI Clipper** — *Create More. Edit Less.*

## 2. What We're Building
An AI-powered web platform that converts long-form videos into engaging, professionally
edited short-form clips (YouTube Shorts, Instagram Reels, TikTok). The AI analyzes content,
finds interesting moments, generates clips, adds captions, recommends music, formats
vertically (9:16), and lets the user fine-tune and export the result.

This is a real product, not a demo — functionality must actually work before being reported
as working.

## 3. Who It's For
- Gamers / streamers clipping livestream highlights
- Podcasters extracting shareable moments
- Sports/cricket commentary channels
- General YouTube creators (tutorials, educational, tech content)

Beginner/intermediate solo developer building this with AI coding tools (Claude, Codex) —
the product must be built incrementally, with each phase fully working before the next.

## 4. Target Content Categories
Each category needs its own highlight-detection logic — one strategy does not fit all.

| Category | What AI should look for |
|---|---|
| Gaming | Funny moments, reactions, wins/losses, epic plays, interesting banter |
| Podcasts | Powerful statements, strong opinions, funny exchanges, educational beats |
| Cricket | Commentary highlights, match analysis, player interviews, exciting moments |
| Other sports | Football/basketball highlights, interviews, analysis, reactions |
| Other | Educational/tutorial/tech content, general highlights |

## 5. Core Features (Product Scope)
1. **Video Input** — upload (drag & drop), authorized source URLs, validation, metadata extraction
2. **AI Highlight Detection** — transcript understanding, topic/emotion shifts, clean cut points, reasoned + scored clip suggestions, auto-decided clip count
3. **Custom Clip Duration** — presets (15–30s, 30–60s, 60–90s) + custom min/max
4. **AI Captions Studio** — word-by-word/sentence captions, styling, presets per category, mobile-readable
5. **Music Studio** — automatic (mood/category-based, licensed) + manual (library, upload, mixing, fades)
6. **Smart Video Editing** — 9:16 conversion, smart crop, face/speaker tracking, zoom, blur, trim, preview
7. **Export System** — 1080×1920 MP4 (H.264), individual/batch export, progress, validated output only

## 6. Non-Goals (for now)
- No unauthorized video downloading or DRM bypassing
- No use of unlicensed/copyrighted music
- No full editing-suite feature parity with professional NLEs
- No multi-platform publishing integrations until later phases (Phase 7+)

## 7. Success Criteria (per phase)
A phase is "done" only when its features work end-to-end, are tested, and are reported
accurately — see `Phases.md` for phase-by-phase acceptance criteria.

## 8. Related Documents
- `Architecture.md` — technical structure and stack
- `Rules.md` — engineering/AI-assistant constraints
- `Phases.md` — delivery roadmap
- `Design.md` — visual language
- `Memory.md` — session/progress log
