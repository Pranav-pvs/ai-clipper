# AI Clipper — Rules & Constraints

These rules are mandatory for both the human developer and any AI assistant (Claude, Codex, etc.) working on this project.

## 1. Repository Safety
- Always inspect the existing repository before changing anything.
- Preserve existing working code; never overwrite files without reading them first.
- Check Git status before making changes; never discard uncommitted work.
- Avoid unnecessary restructuring — explain major structural changes before making them.

## 2. Coding Standards
- Clean, readable, maintainable code with meaningful names.
- No duplicated logic; keep frontend, backend, and processing responsibilities separated.
- Use proper types (TypeScript on frontend, type hints on backend).
- Comment complicated logic. Handle errors properly — no silent failures.

## 3. Security
- Never hardcode API keys — use environment variables, with `.env.example` provided.
- Never commit `.env` files.
- Validate all uploaded files on the backend; restrict file size and processing resources.
- Never expose private storage URLs or credentials.

## 4. Testing
- Test every important feature, including invalid uploads, API responses, and processing errors.
- Never claim functionality works without actually verifying it.

## 5. Dependencies
- No unnecessary libraries — check compatibility before installing.
- Explain the purpose of any major new dependency.
- Prefer stable, maintained packages.

## 6. Performance
- No large video processing in the browser.
- Long-running operations go through background jobs (Celery), not request/response.
- Avoid loading entire large videos into memory; clean up temp files after use.
- Design storage/processing to scale gradually — don't over-engineer early.

## 7. Copyright & Permissions
- Respect video-platform terms of service — no DRM bypass, no unauthorized downloading.
- Only process videos the user owns or has explicit permission to edit.
- Use only licensed, royalty-free, public-domain, or user-authorized music; store license/attribution info where required.
- Never imply that captions, cropping, or effects make copyrighted footage legally reusable.

## 8. Working Process (AI Assistant Behavior)
1. Explain technical concepts in simple English.
2. Work on **one small task at a time** — no dumping thousands of lines unexplained.
3. Inspect existing code before modifying it.
4. Explain the plan before implementing.
5. Implement only the approved task.
6. Run relevant tests.
7. Report exactly what changed and which files were created/modified.
8. State what remains incomplete and the next logical step.
9. Never auto-advance to the next phase — wait for explicit approval.
10. If something fails, investigate the real cause — never hide errors or fake functionality.
11. If a decision is needed from the user, ask one clear question at a time.
12. Break large tasks into smaller milestones.
13. Maintain a progress log (`Memory.md`) so work can resume across sessions/tools.

## 9. Phase Discipline
- Do not skip phases (see `Phases.md`).
- Do not implement advanced AI functionality ahead of its phase.
- Each phase has explicit completion requirements that must be met before moving on.
