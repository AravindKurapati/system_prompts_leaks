# Design: Upstream Sync + Mesh Gradient Background

**Branch:** `cc/sync-and-aesthetics`
**Date:** 2026-03-30

---

## Task 1 — Upstream Sync in GitHub Actions

### Goal
Sync the four prompt folders from the upstream repo (`asgeirtj/system_prompts_leaks`) before the pipeline runs, so `extract_and_analyze.py` always sees the latest prompt files.

### Constraint
Only `Anthropic/`, `OpenAI/`, `Google/`, `xAI/` may be overwritten. `CLAUDE.md`, `frontend/`, `documents/`, `archive/`, and all other repo files must not be touched.

### Implementation

In `.github/workflows/update.yml`, add a new step to the `pipeline` job immediately after `actions/checkout` (before `setup-python`):

```yaml
- name: Sync prompt files from upstream
  run: |
    git remote add upstream https://github.com/asgeirtj/system_prompts_leaks.git || true
    git fetch upstream main || echo "WARNING: Could not reach upstream, running with existing files"
    git checkout upstream/main -- Anthropic/ OpenAI/ Google/ xAI/ || echo "WARNING: Upstream checkout failed, using existing files"
```

**Error handling:** Tolerant. If upstream is unreachable or checkout fails, the pipeline continues with whatever prompt files are already in the repo. The `|| true` on `git remote add` prevents failure when the remote already exists on re-runs.

### Final step order in `pipeline` job

```
actions/checkout (fetch-depth: 0)
→ Sync prompt files from upstream          ← NEW
→ actions/setup-python
→ Install Python deps
→ Debug
→ Run pipeline (extract_and_analyze.py)
→ Commit updated timeline
```

The `deploy` job is unchanged.

---

## Task 2 — Animated Mesh Gradient Background

### Goal
Add a subtle animated mesh gradient to the app background — dark blues and purples bleeding into `#0d1117`. Depth, not decoration. Text and data must remain fully readable.

### Approach

**Technique:** CSS-only `::before` pseudo-element on a `.mesh-root` wrapper div, with three independently animated radial-gradient blobs at different viewport positions. A static top-glow on `body` grounds the page.

**No JS, no libraries. GPU-composited animation (`transform` only).**

### Colors and opacity

Using existing CSS theme variables:
- `#58a6ff` (blue-acc) at ~11% opacity
- `#a371f7` (purple-acc) at ~10% opacity

Against `#0d1117` these are visible as depth without reading as decoration.

### Blob layout

| Blob | Position | Color | Duration |
|------|----------|-------|----------|
| 1 | top-left (15%, 10%) | blue `#58a6ff` | 31s |
| 2 | top-right (85%, 15%) | purple `#a371f7` | 43s |
| 3 | bottom-center (50%, 85%) | purple `#a371f7` | 57s |

Durations are intentionally non-harmonious (31/43/57 share no common factor) so the blobs never re-sync and create a repeating pulse.

### Static top-glow

A non-animating `radial-gradient` on `body`:

```css
background: radial-gradient(ellipse at 50% 0%, rgba(88,166,255,0.05) 0%, transparent 60%), #0d1117;
```

Gives the page a subtle cool atmosphere from the top edge.

### Z-index layering

```
body / .mesh-root                    z-index context
  ::before (mesh blobs)              position: fixed; z-index: 0; pointer-events: none
  app content wrapper                position: relative; z-index: 1
```

### Files changed

| File | Change |
|------|--------|
| `frontend/src/index.css` | Add `.mesh-root::before` rules + static top-glow on `body` |
| `frontend/src/App.jsx` | Wrap outermost `div` in `<div className="mesh-root">` |
