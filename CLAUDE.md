# AI Prompt Watch — Claude Code Context

## What this is
Static dashboard tracking system prompt changes for Claude, ChatGPT, Gemini, Grok.
Pipeline: GitHub Actions → extract_and_analyze.py → enriched_timeline.json → frontend (React + Vite)

## Architecture
- `extract_and_analyze.py`: pulls git history per canonical file, diffs prompts, calls Groq for summaries + behavioral tagging
- `enriched_timeline.json`: generated output consumed by the frontend — never edit directly
- `frontend/`: React + Vite app, reads enriched_timeline.json at runtime, builds to `dist/` for GitHub Pages
- Canonical prompt files: `Anthropic/claude.html`, `OpenAI/GPT-4o.md`, `Google/gemini-workspace.md`, `xAI/grok-4.2.md`

## Before starting any task
- Read `documents/spec.md` before any feature work
- Read `documents/platform-docs.md` before touching extract_and_analyze.py or the JSON schema
- Interview me in detail about technical implementation, tradeoffs, and concerns before writing any code
- Never assume which file to edit if multiple candidates exist

## Rules
- Never commit directly to main — always work on a `cc/task-description` branch
- Never edit `enriched_timeline.json` directly — it is generated output
- Perplexity is excluded from tracking (search/RAG wrapper, not a frontier model)
- After every meaningful change, append a summary to CHANGELOG.md
- Schema changes to enriched_timeline.json affect both pipeline and frontend — flag before touching

## Bug Rule
When a bug is reported, do NOT fix it immediately.
First write a test in `test_pipeline.py` that reproduces the wrong behavior.
Then fix it. Then prove the fix with a passing test.

## Known Gotchas
- Groq rate limits: 2s sleep between summarize calls
- HTML files need tag stripping before any text analysis: `re.sub(r"<[^>]+>", " ", content)`
- OpenAI timeline is currently empty — no commits to GPT-4o.md in tracked window

## What we removed and why (do not re-add)
- Injection resistance scoring — scored Llama simulating the model, not the model itself. Meaningless signal, real API cost. Removed intentionally.
- Synchronized events display — too few data points to be meaningful
- Top words added/removed — polluted by CSS variable names, low signal

## Stack
- Frontend: React + Vite, Tailwind CSS, recharts, react-diff-viewer-continued
- Pipeline: Python, Groq API (llama-3.3-70b-versatile)
- Fonts: Syne (display) + IBM Plex Mono (code/data)
- Colors: `#0d1117` bg, `#3fb950` green, `#f85149` red, `#58a6ff` blue, `#d29922` yellow

## Current state (Mar 2026)
- Perplexity removed from tracking
- index.html is being replaced by React + Vite frontend (see documents/spec.md)
- enriched_timeline.json has real data for claude, gemini, grok (openai empty)
- Pipeline needs: behavioral_tags, content_snapshot, prompt_length fields added (see spec.md Phase 1)