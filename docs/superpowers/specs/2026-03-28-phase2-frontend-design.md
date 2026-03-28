# Phase 2 Frontend Design — AI Prompt Watch

Date: 2026-03-28
Branch: cc/phase2-frontend

---

## Goal

Rebuild the dashboard from a vanilla `index.html` into a React + Vite app that surfaces
system prompt evolution as a research tool for developers and AI researchers.

---

## Layout (decided via visual brainstorming)

Single page. Tab bar at top with **Overview first**, then one tab per model.

```
[ Stats Bar ]
[ Overview | Claude | Gemini | Grok | ChatGPT ]
[ tab content ]
```

- **Overview tab**: all analytics charts + concept composition bars
- **Model tabs**: tag filter bar + timeline of entry cards — no charts

---

## Data

`enriched_timeline.json` fetched from `${import.meta.env.BASE_URL}enriched_timeline.json`.

Schema per entry (Phase 1 output):
```json
{
  "date": "YYYY-MM-DD",
  "commit": "short hash",
  "message": "git commit message",
  "filepath": "...",
  "diff": { "added": [...], "removed": [...], "added_count": N, "removed_count": N, "total_change": N },
  "behavioral_tags": ["safety", "tool_definition"],
  "content_raw": "...",
  "content_snapshot": "HTML-stripped prompt text",
  "prompt_length": N,
  "summary": "Groq plain-English summary"
}
```

Top-level: `generated_at`, `models`, `timelines`, `stats`.

---

## Component Tree

```
App
├── StatsBar
├── Tabs (Radix UI)
│   ├── Tab: Overview
│   │   ├── ChangesBarChart
│   │   ├── PromptLengthChart
│   │   ├── HeatmapChart
│   │   └── ConceptDriftBar (one per model)
│   └── Tab: [model] × 4
│       ├── FilterBar (tag checkboxes)
│       └── Timeline
│           └── EntryCard ×N
│               ├── DiffViewer (inline expand, collapsed by default)
│               └── [triggers FullPromptViewer drawer]
└── FullPromptViewer (drawer, rendered once at App level, shared)
```

---

## Components

### StatsBar
- Shows: models tracked count, total changes across all models, `generated_at` formatted as "last updated YYYY-MM-DD"
- Single horizontal bar, muted text, IBM Plex Mono font

### Tabs
- Radix UI `@radix-ui/react-tabs`
- Tab labels: "Overview", then model display names from MODEL_META
- Active tab: blue underline indicator, white text; inactive: muted

### FilterBar
- One checkbox pill per tag (all 8 tags)
- Default: all selected (show everything)
- Show an entry if its behavioral_tags intersects the active filter set (entry needs at least one checked tag — OR/union logic)
- Visually: row of colored pill checkboxes above the timeline, matching tag colors

### EntryCard — stacked rows layout (A)
```
Row 1: [date]  ·  [commit hash]  ·  [commit message]          [+N  −N]
Row 2: [summary text]
Row 3: [tag badge] [tag badge] ...
Row 4: [▶ diff]  [⊞ full prompt]
       └─ DiffViewer (expands inline below when ▶ diff clicked)
```
- Card background: `#161b22`, border: `#21262d`
- Date/commit in `#8b949e`, hash in `#58a6ff`, summary in `#e6edf3`
- +N in `#3fb950`, −N in `#f85149`
- Actions: ghost buttons, `#8b949e` text, `#21262d` bg

### TagBadge
- Colored pill with border: `background: {color}22`, `border: 1px solid {color}44`, text in tag color
- Tag color map:
  - `safety` → `#f85149`
  - `tool_definition` → `#58a6ff`
  - `persona` → `#a371f7`
  - `capability` → `#3fb950`
  - `formatting` → `#8b949e`
  - `memory` → `#d29922`
  - `policy` → `#e3882a`
  - `other` → `#30363d` (muted)

### DiffViewer
- Uses `react-diff-viewer-continued` in split view, dark theme
- `oldValue`: removed lines joined with `\n`
- `newValue`: added lines joined with `\n`
- Note: partial diff (up to 30 lines each side), not full-document diff — this is a known limitation
- Collapsed by default; toggled by "▶ diff" button on EntryCard

### FullPromptViewer (drawer — layout B)
- Rendered once at App level, controlled via shared state: `{ open: bool, entry: object | null }`
- Slides in from the right, ~45% viewport width
- Header: model name + date + commit hash, Copy button, ✕ close
- Body: scrollable `content_snapshot` text, IBM Plex Mono, `#8b949e` color
- Timeline remains visible and scrollable on the left while drawer is open

### Charts (Overview tab)

**ChangesBarChart** — recharts BarChart
- X: model name, Y: total_changes from stats
- Bar color per model from MODEL_META

**PromptLengthChart** — recharts LineChart
- X: date, Y: prompt_length
- One line per model, color from MODEL_META
- Only models with >1 data point render a line

**HeatmapChart** — CSS grid (no recharts)
- Rows: models, Columns: months (derived from timeline dates)
- Cell color: green intensity scaled to change count that month
- Simple `#0d1117` → `#3fb950` scale, 5 steps

**ConceptDriftBar** — recharts BarChart (layout="vertical", stacked)
- One row per model
- Stacked segments = proportion of changes tagged with each behavioral tag
- Shows "Claude spends X% of changes on safety, Grok on tool_definition" at a glance

---

## Model Metadata

```js
const MODEL_META = {
  claude:  { label: "Claude",   color: "#d97706" },
  openai:  { label: "ChatGPT",  color: "#10a37f" },
  gemini:  { label: "Gemini",   color: "#4285f4" },
  grok:    { label: "Grok",     color: "#9333ea" },
}
```

---

## Design System

- Background: `#0d1117`
- Surface: `#161b22`
- Border: `#21262d`
- Text primary: `#e6edf3`
- Text muted: `#8b949e`
- Fonts: Syne (headings/display), IBM Plex Mono (data/code/body)
- No animations except subtle hover state transitions (100ms)
- Dense layout — this is a developer tool, not a marketing page

---

## Deployment

- Vite base path: `/system_prompts_leaks/`
- GitHub Pages served from `gh-pages` branch
- Actions workflow: two jobs
  1. **pipeline** — runs `extract_and_analyze.py`, commits `enriched_timeline.json` to main
  2. **deploy** (needs: pipeline) — copies JSON to `frontend/public/`, builds Vite, force-pushes `dist/` to gh-pages via `peaceiris/actions-gh-pages`

---

## What We Are NOT Building

- Cross-model compare view (Phase 2b, deferred)
- Backend or API
- User accounts
- Injection resistance scoring (removed in Phase 1)
- Synchronized events display (removed in Phase 1)
- Top words added/removed (removed)
- Perplexity tracking (removed)
