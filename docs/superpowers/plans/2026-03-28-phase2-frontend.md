# Phase 2 Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the React + Vite frontend for AI Prompt Watch — a dark-theme developer dashboard for tracking system prompt changes across frontier AI models.

**Architecture:** Single-page Vite + React app. Tab structure: Overview tab (analytics charts) + one tab per tracked model (timeline of change cards with tag filtering). Data fetched at runtime from static `enriched_timeline.json`. Deployed to `gh-pages` branch via GitHub Actions.

**Tech Stack:** React 18, Vite, Tailwind CSS v3, Radix UI Tabs, recharts, react-diff-viewer-continued, Vitest + @testing-library/react

---

## File Map

```
frontend/
├── index.html                          modified — add Google Fonts
├── vite.config.js                      modified — base path + vitest config
├── tailwind.config.js                  created — design system colors + fonts
├── postcss.config.js                   created
├── .gitignore                          modified — add public/enriched_timeline.json
├── public/
│   └── enriched_timeline.json          copied at build time (not committed)
└── src/
    ├── main.jsx                        unchanged
    ├── index.css                       replaced — Tailwind directives only
    ├── App.jsx                         replaced — full wired layout
    ├── test-setup.js                   created — @testing-library/jest-dom
    ├── hooks/
    │   └── useTimeline.js              created — fetch + parse enriched_timeline.json
    ├── utils/
    │   ├── tagColors.js                created — TAG_COLORS, MODEL_META, filterEntries, computeTagProportions
    │   └── tagColors.test.js           created — unit tests for pure functions
    └── components/
        ├── StatsBar.jsx
        ├── TagBadge.jsx
        ├── FilterBar.jsx
        ├── EntryCard.jsx
        ├── DiffViewer.jsx
        ├── FullPromptViewer.jsx
        ├── Timeline.jsx
        ├── ModelTabs.jsx
        ├── ConceptDriftBar.jsx
        ├── ConceptDriftBar.test.js
        └── charts/
            ├── ChangesBarChart.jsx
            ├── PromptLengthChart.jsx
            └── HeatmapChart.jsx

archive/
└── index_vanilla.html                  moved from index.html

.github/workflows/
└── update.yml                          modified — add deploy job
```

---

### Task 1: Branch + archive old index.html

**Files:**
- Move: `index.html` → `archive/index_vanilla.html`

- [ ] Create branch:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git checkout -b cc/phase2-frontend
```

- [ ] Archive the old index:
```bash
git mv index.html archive/index_vanilla.html
git commit -m "archive vanilla index.html before React + Vite rebuild"
```

---

### Task 2: Scaffold Vite + install all dependencies

**Files:**
- Create: `frontend/` (Vite scaffold)

- [ ] Scaffold:
```bash
cd D:/Aru/NYU/system_prompts_leaks
npm create vite@latest frontend -- --template react
```
Expected: "Scaffolding project in frontend/... Done."

- [ ] Install everything in one pass:
```bash
cd frontend
npm install
npm install recharts react-diff-viewer-continued @radix-ui/react-tabs
npm install -D tailwindcss postcss autoprefixer vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

- [ ] Add test scripts — open `frontend/package.json` and add to `"scripts"`:
```json
"test": "vitest run",
"test:watch": "vitest"
```

- [ ] Verify dev server starts:
```bash
npm run dev
```
Expected: `Local: http://localhost:5173/` — Vite default page loads. Ctrl+C.

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/
git commit -m "scaffold vite react project, install all dependencies"
```

---

### Task 3: Configure Vite, Tailwind, PostCSS, fonts

**Files:**
- Modify: `frontend/vite.config.js`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/postcss.config.js`
- Modify: `frontend/index.html`
- Replace: `frontend/src/index.css`
- Delete: `frontend/src/App.css`
- Create: `frontend/src/test-setup.js`

- [ ] Replace `frontend/vite.config.js`:
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/system_prompts_leaks/',
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test-setup.js',
  },
})
```

- [ ] Create `frontend/tailwind.config.js`:
```js
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        bg:             '#0d1117',
        surface:        '#161b22',
        'border-dim':   '#21262d',
        primary:        '#e6edf3',
        muted:          '#8b949e',
        'green-acc':    '#3fb950',
        'red-acc':      '#f85149',
        'blue-acc':     '#58a6ff',
        'yellow-acc':   '#d29922',
        'purple-acc':   '#a371f7',
        'orange-acc':   '#e3882a',
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        mono:    ['"IBM Plex Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
```

- [ ] Create `frontend/postcss.config.js`:
```js
export default {
  plugins: { tailwindcss: {}, autoprefixer: {} },
}
```

- [ ] Replace `frontend/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Prompt Watch</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Syne:wght@400;600;700&display=swap" rel="stylesheet" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

- [ ] Replace `frontend/src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  background-color: #0d1117;
  color: #e6edf3;
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
}
```

- [ ] Delete Vite's default App.css:
```bash
rm frontend/src/App.css
```

- [ ] Create `frontend/src/test-setup.js`:
```js
import '@testing-library/jest-dom'
```

- [ ] Smoke-test Tailwind — put this in `frontend/src/App.jsx` temporarily:
```jsx
export default function App() {
  return <div className="p-8 font-display text-2xl text-blue-acc">Tailwind + Syne working</div>
}
```
Run `npm run dev`, confirm blue Syne text. Ctrl+C.

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/
git commit -m "configure vite base path, tailwind design system, postcss, google fonts"
```

---

### Task 4: Data layer — tagColors.js + useTimeline.js with tests

**Files:**
- Create: `frontend/src/utils/tagColors.js`
- Create: `frontend/src/utils/tagColors.test.js`
- Create: `frontend/src/hooks/useTimeline.js`

- [ ] Create `frontend/src/utils/tagColors.js`:
```js
export const TAG_COLORS = {
  safety:          '#f85149',
  tool_definition: '#58a6ff',
  persona:         '#a371f7',
  capability:      '#3fb950',
  formatting:      '#8b949e',
  memory:          '#d29922',
  policy:          '#e3882a',
  other:           '#30363d',
}

export const MODEL_META = {
  claude:  { label: 'Claude',  color: '#d97706' },
  openai:  { label: 'ChatGPT', color: '#10a37f' },
  gemini:  { label: 'Gemini',  color: '#4285f4' },
  grok:    { label: 'Grok',    color: '#9333ea' },
}

export const ALL_TAGS = Object.keys(TAG_COLORS)

/**
 * Filter entries by active tag set.
 * OR logic: entry passes if it has at least one tag in activeTags.
 */
export function filterEntries(entries, activeTags) {
  if (activeTags.size === ALL_TAGS.length) return entries
  if (activeTags.size === 0) return []
  return entries.filter(e =>
    Array.isArray(e.behavioral_tags) &&
    e.behavioral_tags.some(t => activeTags.has(t))
  )
}

/**
 * Proportion of entries tagged with each tag (0.0–1.0+).
 * Proportions may sum above 1 — entries can carry multiple tags.
 */
export function computeTagProportions(entries) {
  if (!entries || entries.length === 0) return {}
  const counts = Object.fromEntries(ALL_TAGS.map(t => [t, 0]))
  for (const entry of entries) {
    for (const tag of (entry.behavioral_tags || [])) {
      if (tag in counts) counts[tag]++
    }
  }
  return Object.fromEntries(
    Object.entries(counts).map(([tag, n]) => [tag, n / entries.length])
  )
}
```

- [ ] Create `frontend/src/utils/tagColors.test.js`:
```js
import { describe, it, expect } from 'vitest'
import { filterEntries, computeTagProportions, ALL_TAGS } from './tagColors'

const e = (tags) => ({ behavioral_tags: tags })

describe('filterEntries', () => {
  it('returns all entries when all tags active', () => {
    const result = filterEntries([e(['safety']), e(['policy'])], new Set(ALL_TAGS))
    expect(result).toHaveLength(2)
  })

  it('returns empty when no tags active', () => {
    expect(filterEntries([e(['safety'])], new Set())).toHaveLength(0)
  })

  it('OR logic — entry with any matching tag passes', () => {
    const entries = [e(['safety', 'policy']), e(['persona']), e(['other'])]
    const result = filterEntries(entries, new Set(['safety', 'persona']))
    expect(result).toHaveLength(2)
  })

  it('filters to exact match', () => {
    const entries = [e(['safety']), e(['policy']), e(['persona'])]
    expect(filterEntries(entries, new Set(['safety']))).toHaveLength(1)
  })

  it('handles missing behavioral_tags gracefully', () => {
    expect(filterEntries([{ behavioral_tags: undefined }], new Set(['safety']))).toHaveLength(0)
  })
})

describe('computeTagProportions', () => {
  it('returns empty for empty entries', () => {
    expect(computeTagProportions([])).toEqual({})
  })

  it('correct proportion for single-tagged entries', () => {
    const entries = [e(['safety']), e(['safety']), e(['policy'])]
    const p = computeTagProportions(entries)
    expect(p.safety).toBeCloseTo(2 / 3)
    expect(p.policy).toBeCloseTo(1 / 3)
    expect(p.persona).toBe(0)
  })

  it('proportions sum above 1 for multi-tagged entries', () => {
    const p = computeTagProportions([e(['safety', 'policy'])])
    expect(Object.values(p).reduce((a, b) => a + b, 0)).toBeGreaterThan(1)
  })
})
```

- [ ] Run tests:
```bash
cd frontend && npm test
```
Expected: all tests **PASS**.

- [ ] Create `frontend/src/hooks/useTimeline.js`:
```js
import { useState, useEffect } from 'react'

export function useTimeline() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}enriched_timeline.json`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then(setData)
      .catch(setError)
  }, [])

  return { data, error }
}
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/
git commit -m "data layer: tagColors utils, filterEntries, computeTagProportions with tests, useTimeline hook"
```

---

### Task 5: StatsBar + TagBadge + smoke test with real data

**Files:**
- Create: `frontend/src/components/StatsBar.jsx`
- Create: `frontend/src/components/TagBadge.jsx`

- [ ] Create `frontend/src/components/StatsBar.jsx`:
```jsx
export default function StatsBar({ data }) {
  if (!data) return null
  const total = Object.values(data.stats).reduce((s, m) => s + m.total_changes, 0)
  const updated = data.generated_at?.slice(0, 10) ?? '—'
  return (
    <div className="flex items-center gap-4 px-6 py-2.5 border-b border-border-dim text-muted font-mono text-xs">
      <span><span className="text-primary">{data.models.length}</span> models</span>
      <span className="text-border-dim">·</span>
      <span><span className="text-primary">{total}</span> changes</span>
      <span className="text-border-dim">·</span>
      <span>updated <span className="text-primary">{updated}</span></span>
    </div>
  )
}
```

- [ ] Create `frontend/src/components/TagBadge.jsx`:
```jsx
import { TAG_COLORS } from '../utils/tagColors'

export default function TagBadge({ tag }) {
  const color = TAG_COLORS[tag] ?? TAG_COLORS.other
  return (
    <span
      className="text-xs px-2 py-0.5 rounded-full border font-mono"
      style={{ color, backgroundColor: `${color}22`, borderColor: `${color}44` }}
    >
      {tag}
    </span>
  )
}
```

- [ ] Copy JSON to public dir for local dev (not committed — just for dev server):
```bash
cp D:/Aru/NYU/system_prompts_leaks/enriched_timeline.json D:/Aru/NYU/system_prompts_leaks/frontend/public/enriched_timeline.json
```

- [ ] Wire up StatsBar in `frontend/src/App.jsx` to verify real data loads:
```jsx
import { useTimeline } from './hooks/useTimeline'
import StatsBar from './components/StatsBar'

export default function App() {
  const { data, error } = useTimeline()
  if (error) return <div className="p-8 text-red-acc font-mono text-sm">Error: {error.message}</div>
  if (!data) return <div className="p-8 text-muted font-mono text-sm">Loading...</div>
  return (
    <div className="min-h-screen bg-bg">
      <StatsBar data={data} />
      <p className="px-6 py-4 font-mono text-xs text-muted">models: {data.models.join(', ')}</p>
    </div>
  )
}
```

- [ ] Verify:
```bash
cd frontend && npm run dev
```
Expected: StatsBar renders real model count + change count. Ctrl+C.

- [ ] Add `public/enriched_timeline.json` to `frontend/.gitignore`:
Open `frontend/.gitignore` (Vite creates one) and add:
```
public/enriched_timeline.json
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/components/ frontend/.gitignore
git commit -m "add StatsBar, TagBadge; smoke test with real JSON confirms data layer works"
```

---

### Task 6: FilterBar

**Files:**
- Create: `frontend/src/components/FilterBar.jsx`

- [ ] Create `frontend/src/components/FilterBar.jsx`:
```jsx
import { ALL_TAGS, TAG_COLORS } from '../utils/tagColors'

export default function FilterBar({ activeTags, onToggle, onSelectAll, onClearAll }) {
  const allActive = activeTags.size === ALL_TAGS.length
  return (
    <div className="flex flex-wrap items-center gap-2 py-3">
      <span className="text-muted font-mono text-xs">filter:</span>
      {ALL_TAGS.map(tag => {
        const active = activeTags.has(tag)
        const color = TAG_COLORS[tag]
        return (
          <button
            key={tag}
            onClick={() => onToggle(tag)}
            className="text-xs px-2 py-0.5 rounded-full border font-mono transition-all"
            style={{
              color:           active ? color : '#8b949e',
              backgroundColor: active ? `${color}22` : 'transparent',
              borderColor:     active ? `${color}44` : '#21262d',
              opacity:         active ? 1 : 0.5,
            }}
          >
            {tag}
          </button>
        )
      })}
      <button
        onClick={allActive ? onClearAll : onSelectAll}
        className="text-xs text-muted hover:text-primary font-mono ml-1 underline underline-offset-2"
      >
        {allActive ? 'clear all' : 'select all'}
      </button>
    </div>
  )
}
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/components/FilterBar.jsx
git commit -m "add FilterBar component"
```

---

### Task 7: DiffViewer

**Files:**
- Create: `frontend/src/components/DiffViewer.jsx`

- [ ] Create `frontend/src/components/DiffViewer.jsx`:
```jsx
import ReactDiffViewer from 'react-diff-viewer-continued'

const STYLES = {
  variables: {
    dark: {
      diffViewerBackground:  '#0d1117',
      addedBackground:       '#0e4429',
      addedColor:            '#3fb950',
      removedBackground:     '#4b1113',
      removedColor:          '#f85149',
      wordAddedBackground:   '#1a7f37',
      wordRemovedBackground: '#7d2026',
      gutterBackground:      '#161b22',
      gutterColor:           '#8b949e',
    },
  },
}

export default function DiffViewer({ diff }) {
  const oldValue = (diff.removed || []).join('\n')
  const newValue = (diff.added   || []).join('\n')
  const truncated = (diff.added_count ?? 0) > 30 || (diff.removed_count ?? 0) > 30

  return (
    <div className="mt-3">
      <ReactDiffViewer
        oldValue={oldValue}
        newValue={newValue}
        splitView={true}
        useDarkTheme={true}
        styles={STYLES}
        leftTitle="removed"
        rightTitle="added"
      />
      <p className="text-xs text-muted font-mono mt-1.5">
        {truncated
          ? `showing first 30 of ${Math.max(diff.added_count ?? 0, diff.removed_count ?? 0)} changed lines`
          : 'showing all changed lines'}
      </p>
    </div>
  )
}
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/components/DiffViewer.jsx
git commit -m "add DiffViewer wrapping react-diff-viewer-continued"
```

---

### Task 8: EntryCard

**Files:**
- Create: `frontend/src/components/EntryCard.jsx`

- [ ] Create `frontend/src/components/EntryCard.jsx`:
```jsx
import { useState } from 'react'
import TagBadge from './TagBadge'
import DiffViewer from './DiffViewer'

export default function EntryCard({ entry, modelName, onViewPrompt }) {
  const [showDiff, setShowDiff] = useState(false)

  return (
    <div className="bg-surface border border-border-dim rounded-md p-4 mb-3">
      {/* Row 1: date · commit · message  +N −N */}
      <div className="flex items-start justify-between gap-4 mb-2">
        <div className="font-mono text-xs text-muted flex flex-wrap items-center gap-1.5 min-w-0">
          <span className="shrink-0">{entry.date}</span>
          <span className="text-border-dim">·</span>
          <span className="text-blue-acc shrink-0">{entry.commit}</span>
          <span className="text-border-dim">·</span>
          <span className="truncate">{entry.message}</span>
        </div>
        <div className="font-mono text-xs flex gap-3 shrink-0">
          <span className="text-green-acc">+{entry.diff?.added_count ?? 0}</span>
          <span className="text-red-acc">−{entry.diff?.removed_count ?? 0}</span>
        </div>
      </div>

      {/* Row 2: summary */}
      <p className="text-sm text-primary leading-relaxed mb-2">
        {entry.summary ?? <span className="text-muted italic">No summary available.</span>}
      </p>

      {/* Row 3: tag badges */}
      {entry.behavioral_tags?.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {entry.behavioral_tags.map(tag => <TagBadge key={tag} tag={tag} />)}
        </div>
      )}

      {/* Row 4: actions */}
      <div className="flex gap-2">
        <button
          onClick={() => setShowDiff(v => !v)}
          className="text-xs font-mono px-3 py-1 bg-bg border border-border-dim text-muted hover:text-primary rounded transition-colors"
        >
          {showDiff ? '▼ hide diff' : '▶ diff'}
        </button>
        <button
          onClick={() => onViewPrompt(entry, modelName)}
          className="text-xs font-mono px-3 py-1 bg-bg border border-border-dim text-muted hover:text-primary rounded transition-colors"
        >
          ⊞ full prompt
        </button>
      </div>

      {showDiff && <DiffViewer diff={entry.diff} />}
    </div>
  )
}
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/components/EntryCard.jsx
git commit -m "add EntryCard with diff toggle"
```

---

### Task 9: FullPromptViewer drawer

**Files:**
- Create: `frontend/src/components/FullPromptViewer.jsx`

- [ ] Create `frontend/src/components/FullPromptViewer.jsx`:
```jsx
import { useEffect } from 'react'
import { MODEL_META } from '../utils/tagColors'

export default function FullPromptViewer({ entry, modelName, onClose }) {
  const label = MODEL_META[modelName]?.label ?? modelName

  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  function handleCopy() {
    navigator.clipboard.writeText(entry.content_snapshot ?? '')
  }

  return (
    <>
      <div className="fixed inset-0 bg-black/40 z-40" onClick={onClose} />
      <div className="fixed top-0 right-0 h-full w-[45vw] min-w-80 bg-surface border-l border-border-dim z-50 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-border-dim shrink-0">
          <span className="font-mono text-xs">
            <span className="text-blue-acc">{label}</span>
            <span className="text-muted"> · {entry.date} · {entry.commit}</span>
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="text-xs font-mono px-3 py-1 bg-bg border border-border-dim text-muted hover:text-primary rounded transition-colors"
            >
              copy
            </button>
            <button onClick={onClose} className="text-muted hover:text-primary text-base px-1 leading-none">
              ✕
            </button>
          </div>
        </div>
        {/* Body */}
        <div className="flex-1 overflow-y-auto px-4 py-4">
          <pre className="font-mono text-xs text-primary leading-relaxed whitespace-pre-wrap break-words">
            {entry.content_snapshot ?? 'No prompt content available.'}
          </pre>
        </div>
      </div>
    </>
  )
}
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/components/FullPromptViewer.jsx
git commit -m "add FullPromptViewer right-side drawer"
```

---

### Task 10: Timeline + ModelTabs

**Files:**
- Create: `frontend/src/components/Timeline.jsx`
- Create: `frontend/src/components/ModelTabs.jsx`

- [ ] Create `frontend/src/components/Timeline.jsx`:
```jsx
import { useState } from 'react'
import { ALL_TAGS, filterEntries } from '../utils/tagColors'
import FilterBar from './FilterBar'
import EntryCard from './EntryCard'

export default function Timeline({ entries, modelName, onViewPrompt }) {
  const [activeTags, setActiveTags] = useState(new Set(ALL_TAGS))

  function toggle(tag) {
    setActiveTags(prev => {
      const next = new Set(prev)
      next.has(tag) ? next.delete(tag) : next.add(tag)
      return next
    })
  }

  const filtered = filterEntries(entries, activeTags)

  return (
    <div>
      <FilterBar
        activeTags={activeTags}
        onToggle={toggle}
        onSelectAll={() => setActiveTags(new Set(ALL_TAGS))}
        onClearAll={() => setActiveTags(new Set())}
      />
      {filtered.length === 0 ? (
        <p className="text-muted font-mono text-sm py-12 text-center">
          No entries match the active filters.
        </p>
      ) : (
        filtered.map((entry, i) => (
          <EntryCard
            key={`${entry.commit}-${i}`}
            entry={entry}
            modelName={modelName}
            onViewPrompt={onViewPrompt}
          />
        ))
      )}
    </div>
  )
}
```

- [ ] Create `frontend/src/components/ModelTabs.jsx`:
```jsx
import * as Tabs from '@radix-ui/react-tabs'
import { MODEL_META } from '../utils/tagColors'
import Timeline from './Timeline'

export default function ModelTabs({ timelines, overviewContent, onViewPrompt }) {
  const modelKeys = Object.keys(MODEL_META)

  return (
    <Tabs.Root defaultValue="overview" className="flex-1">
      <Tabs.List className="flex border-b border-border-dim px-6 overflow-x-auto">
        {[
          { value: 'overview', label: 'Overview', count: null },
          ...modelKeys.map(k => ({
            value: k,
            label: MODEL_META[k].label,
            count: timelines[k]?.length ?? 0,
          })),
        ].map(({ value, label, count }) => (
          <Tabs.Trigger
            key={value}
            value={value}
            className="font-display text-sm px-4 py-3 text-muted shrink-0 border-b-2 border-transparent data-[state=active]:text-primary data-[state=active]:border-blue-acc -mb-px transition-colors whitespace-nowrap"
          >
            {label}
            {count !== null && (
              <span className="ml-1.5 font-mono text-xs text-muted">{count}</span>
            )}
          </Tabs.Trigger>
        ))}
      </Tabs.List>

      <div className="px-6 py-4">
        <Tabs.Content value="overview">{overviewContent}</Tabs.Content>
        {modelKeys.map(key => (
          <Tabs.Content key={key} value={key}>
            <Timeline
              entries={timelines[key] ?? []}
              modelName={key}
              onViewPrompt={onViewPrompt}
            />
          </Tabs.Content>
        ))}
      </div>
    </Tabs.Root>
  )
}
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/components/Timeline.jsx frontend/src/components/ModelTabs.jsx
git commit -m "add Timeline and ModelTabs components"
```

---

### Task 11: Charts — ChangesBarChart + PromptLengthChart

**Files:**
- Create: `frontend/src/components/charts/ChangesBarChart.jsx`
- Create: `frontend/src/components/charts/PromptLengthChart.jsx`

- [ ] Create `frontend/src/components/charts/ChangesBarChart.jsx`:
```jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { MODEL_META } from '../../utils/tagColors'

const TOOLTIP = {
  contentStyle: { background: '#161b22', border: '1px solid #21262d', borderRadius: 4 },
  labelStyle:   { color: '#e6edf3', fontFamily: 'IBM Plex Mono', fontSize: 11 },
  itemStyle:    { color: '#8b949e', fontFamily: 'IBM Plex Mono', fontSize: 11 },
  cursor:       { fill: '#21262d' },
}

export default function ChangesBarChart({ stats }) {
  const data = Object.entries(stats).map(([key, s]) => ({
    name:    MODEL_META[key]?.label ?? key,
    changes: s.total_changes,
    color:   MODEL_META[key]?.color ?? '#8b949e',
  }))

  return (
    <div>
      <h3 className="font-display text-xs text-muted uppercase tracking-widest mb-3">Changes per model</h3>
      <ResponsiveContainer width="100%" height={160}>
        <BarChart data={data} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
          <XAxis dataKey="name" tick={{ fill: '#8b949e', fontSize: 11, fontFamily: 'IBM Plex Mono' }} axisLine={false} tickLine={false} />
          <YAxis allowDecimals={false} tick={{ fill: '#8b949e', fontSize: 11, fontFamily: 'IBM Plex Mono' }} axisLine={false} tickLine={false} />
          <Tooltip {...TOOLTIP} />
          <Bar dataKey="changes" radius={[2, 2, 0, 0]}>
            {data.map((d, i) => <Cell key={i} fill={d.color} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
```

- [ ] Create `frontend/src/components/charts/PromptLengthChart.jsx`:
```jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { MODEL_META } from '../../utils/tagColors'

const TOOLTIP = {
  contentStyle: { background: '#161b22', border: '1px solid #21262d', borderRadius: 4 },
  labelStyle:   { color: '#e6edf3', fontFamily: 'IBM Plex Mono', fontSize: 10 },
  itemStyle:    { fontFamily: 'IBM Plex Mono', fontSize: 10 },
  cursor:       { stroke: '#21262d' },
}

export default function PromptLengthChart({ timelines }) {
  const allDates = new Set()
  const byModel = {}

  for (const [model, entries] of Object.entries(timelines)) {
    if (!entries || entries.length < 2) continue
    byModel[model] = {}
    for (const entry of entries) {
      if (entry.prompt_length != null) {
        allDates.add(entry.date)
        byModel[model][entry.date] = entry.prompt_length
      }
    }
  }

  const models = Object.keys(byModel)
  if (models.length === 0) return (
    <div>
      <h3 className="font-display text-xs text-muted uppercase tracking-widest mb-3">Prompt length over time</h3>
      <p className="text-muted font-mono text-xs">No prompt length data available yet. Re-run the pipeline to generate it.</p>
    </div>
  )

  const chartData = [...allDates].sort().map(date => {
    const point = { date }
    for (const m of models) {
      if (byModel[m][date] != null) point[m] = byModel[m][date]
    }
    return point
  })

  return (
    <div>
      <h3 className="font-display text-xs text-muted uppercase tracking-widest mb-3">Prompt length over time</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
          <XAxis dataKey="date" tick={{ fill: '#8b949e', fontSize: 10, fontFamily: 'IBM Plex Mono' }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: '#8b949e', fontSize: 10, fontFamily: 'IBM Plex Mono' }} axisLine={false} tickLine={false} />
          <Tooltip {...TOOLTIP} />
          <Legend wrapperStyle={{ fontSize: 10, fontFamily: 'IBM Plex Mono', color: '#8b949e' }} />
          {models.map(m => (
            <Line key={m} type="monotone" dataKey={m} name={MODEL_META[m]?.label ?? m}
              stroke={MODEL_META[m]?.color ?? '#8b949e'} strokeWidth={1.5} dot={false} connectNulls={false} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/components/charts/
git commit -m "add ChangesBarChart and PromptLengthChart"
```

---

### Task 12: Charts — HeatmapChart + ConceptDriftBar

**Files:**
- Create: `frontend/src/components/charts/HeatmapChart.jsx`
- Create: `frontend/src/components/ConceptDriftBar.jsx`
- Create: `frontend/src/components/ConceptDriftBar.test.js`

- [ ] Write failing test first in `frontend/src/components/ConceptDriftBar.test.js`:
```js
import { describe, it, expect } from 'vitest'
import { computeTagProportions } from '../utils/tagColors'

describe('computeTagProportions used by ConceptDriftBar', () => {
  it('all zeros for empty entries', () => {
    expect(computeTagProportions([])).toEqual({})
  })

  it('untagged tags have proportion 0', () => {
    const p = computeTagProportions([{ behavioral_tags: ['safety'] }])
    expect(p.safety).toBe(1)
    expect(p.policy).toBe(0)
  })

  it('proportions sum above 1 for multi-tagged entries', () => {
    const p = computeTagProportions([{ behavioral_tags: ['safety', 'policy'] }])
    expect(Object.values(p).reduce((a, b) => a + b, 0)).toBeGreaterThan(1)
  })
})
```

- [ ] Run tests to confirm pass:
```bash
cd frontend && npm test
```
Expected: all tests PASS (function defined in Task 4).

- [ ] Create `frontend/src/components/charts/HeatmapChart.jsx`:
```jsx
import { MODEL_META } from '../../utils/tagColors'

function heatColor(n) {
  if (n === 0) return '#0d1117'
  if (n === 1) return '#0e4429'
  if (n === 2) return '#006d32'
  if (n <= 4) return '#26a641'
  return '#3fb950'
}

export default function HeatmapChart({ timelines }) {
  const allMonths = new Set()
  const modelData = {}

  for (const [model, entries] of Object.entries(timelines)) {
    modelData[model] = {}
    for (const entry of (entries || [])) {
      const month = entry.date?.slice(0, 7)
      if (month) {
        allMonths.add(month)
        modelData[model][month] = (modelData[model][month] ?? 0) + 1
      }
    }
  }

  const months = [...allMonths].sort()
  const models = Object.keys(MODEL_META).filter(m => (timelines[m]?.length ?? 0) > 0)

  if (months.length === 0) return null

  return (
    <div>
      <h3 className="font-display text-xs text-muted uppercase tracking-widest mb-3">Changes by month</h3>
      <div className="overflow-x-auto">
        <table className="text-xs font-mono border-separate" style={{ borderSpacing: 3 }}>
          <thead>
            <tr>
              <th className="w-20 text-right pr-3 font-normal text-muted" />
              {months.map(m => (
                <th key={m} className="font-normal text-muted px-0.5" style={{ minWidth: 26 }}>
                  {m.slice(5)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {models.map(model => (
              <tr key={model}>
                <td className="text-right pr-3 text-muted">{MODEL_META[model].label}</td>
                {months.map(m => {
                  const n = modelData[model]?.[m] ?? 0
                  return (
                    <td key={m} title={`${n} change${n !== 1 ? 's' : ''}`}>
                      <div className="rounded-sm" style={{ width: 22, height: 22, background: heatColor(n) }} />
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
```

- [ ] Create `frontend/src/components/ConceptDriftBar.jsx`:
```jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TAG_COLORS, MODEL_META, ALL_TAGS, computeTagProportions } from '../utils/tagColors'

export default function ConceptDriftBar({ timelines }) {
  const models = Object.keys(MODEL_META).filter(m => (timelines[m]?.length ?? 0) > 0)
  if (models.length === 0) return null

  const data = models.map(model => {
    const p = computeTagProportions(timelines[model] ?? [])
    const row = { model: MODEL_META[model].label }
    for (const tag of ALL_TAGS) row[tag] = Math.round((p[tag] ?? 0) * 100)
    return row
  })

  return (
    <div>
      <h3 className="font-display text-xs text-muted uppercase tracking-widest mb-1">Tag composition per model</h3>
      <p className="text-xs text-muted font-mono mb-3">
        % of changes per category · tags are not mutually exclusive — proportions may sum above 100%
      </p>
      <ResponsiveContainer width="100%" height={models.length * 48 + 40}>
        <BarChart data={data} layout="vertical" margin={{ top: 0, right: 40, left: 50, bottom: 0 }}>
          <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fill: '#8b949e', fontSize: 10, fontFamily: 'IBM Plex Mono' }} axisLine={false} tickLine={false} />
          <YAxis type="category" dataKey="model" width={48} tick={{ fill: '#8b949e', fontSize: 11, fontFamily: 'IBM Plex Mono' }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{ background: '#161b22', border: '1px solid #21262d', borderRadius: 4 }}
            itemStyle={{ fontFamily: 'IBM Plex Mono', fontSize: 10 }}
            formatter={v => [`${v}%`]}
            cursor={{ fill: '#21262d40' }}
          />
          <Legend wrapperStyle={{ fontSize: 10, fontFamily: 'IBM Plex Mono', color: '#8b949e' }} />
          {ALL_TAGS.map(tag => (
            <Bar key={tag} dataKey={tag} name={tag} stackId="a" fill={TAG_COLORS[tag]} maxBarSize={20} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
```

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/components/ConceptDriftBar.jsx frontend/src/components/ConceptDriftBar.test.js frontend/src/components/charts/HeatmapChart.jsx
git commit -m "add HeatmapChart and ConceptDriftBar with tests"
```

---

### Task 13: Wire App.jsx

**Files:**
- Replace: `frontend/src/App.jsx`

- [ ] Replace `frontend/src/App.jsx` with the final layout:
```jsx
import { useState } from 'react'
import { useTimeline } from './hooks/useTimeline'
import StatsBar from './components/StatsBar'
import ModelTabs from './components/ModelTabs'
import FullPromptViewer from './components/FullPromptViewer'
import ChangesBarChart from './components/charts/ChangesBarChart'
import PromptLengthChart from './components/charts/PromptLengthChart'
import HeatmapChart from './components/charts/HeatmapChart'
import ConceptDriftBar from './components/ConceptDriftBar'

function OverviewTab({ data }) {
  return (
    <div className="grid gap-10">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <ChangesBarChart stats={data.stats} />
        <PromptLengthChart timelines={data.timelines} />
      </div>
      <HeatmapChart timelines={data.timelines} />
      <ConceptDriftBar timelines={data.timelines} />
    </div>
  )
}

export default function App() {
  const { data, error } = useTimeline()
  const [drawer, setDrawer] = useState({ open: false, entry: null, modelName: null })

  if (error) return (
    <div className="min-h-screen bg-bg flex items-center justify-center">
      <p className="font-mono text-red-acc text-sm">Failed to load: {error.message}</p>
    </div>
  )
  if (!data) return (
    <div className="min-h-screen bg-bg flex items-center justify-center">
      <p className="font-mono text-muted text-sm">Loading…</p>
    </div>
  )

  return (
    <div className="min-h-screen bg-bg text-primary">
      <header className="px-6 py-4 border-b border-border-dim">
        <h1 className="font-display text-lg font-semibold">AI Prompt Watch</h1>
        <p className="text-muted text-xs font-mono mt-0.5">
          tracking system prompt changes across frontier AI models
        </p>
      </header>

      <StatsBar data={data} />

      <ModelTabs
        timelines={data.timelines}
        onViewPrompt={(entry, modelName) => setDrawer({ open: true, entry, modelName })}
        overviewContent={<OverviewTab data={data} />}
      />

      {drawer.open && drawer.entry && (
        <FullPromptViewer
          entry={drawer.entry}
          modelName={drawer.modelName}
          onClose={() => setDrawer({ open: false, entry: null, modelName: null })}
        />
      )}
    </div>
  )
}
```

- [ ] Full visual check:
```bash
cd frontend && npm run dev
```
Verify: StatsBar populated · Overview tab shows charts · model tabs filter timeline · "▶ diff" toggles · "⊞ full prompt" opens drawer · Escape closes drawer · copy button works.

- [ ] Run all tests:
```bash
npm test
```
Expected: all tests **PASS**.

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add frontend/src/App.jsx
git commit -m "wire all components in App.jsx — full dashboard functional"
```

---

### Task 14: Update GitHub Actions workflow

**Files:**
- Replace: `.github/workflows/update.yml`

- [ ] Replace `.github/workflows/update.yml`:
```yaml
name: Update Timeline and Deploy

on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Python deps
        run: pip install groq python-dotenv

      - name: Debug
        run: |
          pwd && ls
          git log --oneline -5 -- Anthropic/claude.html

      - name: Run pipeline
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        run: python extract_and_analyze.py

      - name: Commit updated timeline
        run: |
          git config --global user.email "action@github.com"
          git config --global user.name "GitHub Action"
          git add enriched_timeline.json
          git diff --staged --quiet || git commit -m "Update timeline $(date +%Y-%m-%d)"
          git push

  deploy:
    needs: pipeline
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          ref: main
          fetch-depth: 1

      - name: Copy JSON to Vite public dir
        run: cp enriched_timeline.json frontend/public/enriched_timeline.json

      - uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install frontend deps
        run: cd frontend && npm ci

      - name: Build
        run: cd frontend && npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/dist
```

- [ ] Validate YAML syntax:
```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/update.yml')); print('valid')"
```
Expected: `valid`

- [ ] Commit:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add .github/workflows/update.yml
git commit -m "split actions workflow into pipeline + deploy jobs, deploy to gh-pages branch"
```

---

### Task 15: Final verification + CHANGELOG + push PR

- [ ] Production build — no errors:
```bash
cd frontend && npm run build
```
Expected: `✓ built in Xs` — `dist/` created, no errors.

- [ ] All tests pass:
```bash
npm test
```
Expected: all **PASS**.

- [ ] Append to `CHANGELOG.md` at the top (after the `# CHANGELOG` heading):
```markdown
## 2026-03-28 — Phase 2 frontend (branch: cc/phase2-frontend)

### New: React + Vite frontend (frontend/)
- Vite + React 18, Tailwind CSS v3, dark theme (`#0d1117` bg)
- Fonts: Syne (headings/tabs), IBM Plex Mono (data/commits), system-ui (body text)
- Layout: Overview tab (analytics) + per-model tabs (timelines only)
- StatsBar, TagBadge, FilterBar (OR-logic tag filter)
- EntryCard: stacked row layout — date/commit → summary → tags → diff/prompt actions
- DiffViewer: react-diff-viewer-continued, split view, "first 30 lines" truncation label
- FullPromptViewer: right-side drawer, content_snapshot, copy button, Escape closes
- ChangesBarChart, PromptLengthChart (recharts), HeatmapChart (CSS grid), ConceptDriftBar
- ConceptDriftBar: footnote that proportions may sum >100% (non-exclusive tags)

### Updated: GitHub Actions (.github/workflows/update.yml)
- Two jobs: pipeline (runs Python, commits JSON) → deploy (needs: pipeline)
- Deploy: copies enriched_timeline.json to frontend/public/, builds Vite, pushes dist/ to gh-pages via peaceiris/actions-gh-pages

### Archived
- index.html → archive/index_vanilla.html
```

- [ ] Commit and push:
```bash
cd D:/Aru/NYU/system_prompts_leaks
git add CHANGELOG.md
git commit -m "add changelog entry for phase 2"
git push -u origin cc/phase2-frontend
```

- [ ] Create PR:
```bash
gh pr create \
  --title "Phase 2: React + Vite frontend rebuild" \
  --base main \
  --body "Full rebuild of the dashboard from vanilla index.html to React + Vite. See CHANGELOG.md for complete list of changes. Deploy workflow pushes to gh-pages on every pipeline run."
```
