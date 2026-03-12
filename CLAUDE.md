# AI Prompt Watch - Claude Code Context

## What this is
Static dashboard tracking system prompt changes for Claude, ChatGPT, Gemini, Grok.
Pipeline: GitHub Actions -> extract_and_analyze.py -> enriched_timeline.json -> index.html

## Rules
- When reporting a bug, write a test in test_pipeline.py that reproduces it first
- After every meaningful change, append a summary to CHANGELOG.md
- Never edit enriched_timeline.json directly - it's generated output
- Perplexity is excluded (search wrapper, not a frontier model)

## Architecture
- extract_and_analyze.py: pulls git history, diffs prompts, calls Groq for summaries + injection scoring
- Injection scoring: llama-3.3-70b simulates the model, we check refusal vs compliance signals
- index.html: pure vanilla JS, reads enriched_timeline.json at runtime, no build step

## Known gotchas
- injection_score goes on timeline[0] (most recent), not timeline[-1]
- Groq rate limits: 2s sleep between summarize calls, 1s between injection tests
- HTML files need HTML tag stripping before injection scoring (re.sub)

## Current state (Mar 2026)
- Perplexity removed from tracking
- Injection scoring fixed (score goes to timeline[0], not timeline[-1])
- index.html redesigned - no build step, pure vanilla JS
- enriched_timeline.json has real data for claude, gemini, grok (openai empty)

## Working style
- Interview me in detail using AskUserQuestion about technical implementation, tradeoffs, and concerns before writing any code
- Never assume which file to edit if multiple candidates exist.