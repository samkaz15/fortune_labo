# Prompt — Rewrite vs New Decision

## Task
For a given intent, decide whether to rewrite an existing page or create a new
URL. **The default answer is rewrite.**

## Why the default is rewrite

Page-count growth is explicitly not progress (`../../seo/kpi.md`). A new URL
splits topical authority, risks cannibalisation, adds a page that must be
maintained forever, and consumes practitioner capacity that could have improved
something already ranking.

## Step 1 — Find every candidate

Search published URLs, `content/briefs/`, and `content/drafts/` for the primary
keyword, its cluster, its synonyms, and the underlying reader question. Report
all matches, not just the closest.

## Step 2 — Score each candidate

| Signal | Favours rewrite | Favours new |
| --- | --- | --- |
| Intent match | Existing page serves the same reader state | Materially different reader state |
| Position | 5–20 with impressions | Not ranking at all *and* off-topic |
| Freshness | Time-bound facts stale | n/a |
| Structure | Outline salvageable | Would require replacing >70% of the page |
| Cannibalisation | Two pages already compete | No overlap |
| Cluster | Fits an existing hub | Requires a new hub (defer instead) |

## Step 3 — Decide

- **`refresh_only`** — structure sound, only dates/facts/prices stale
- **`rewrite`** — intent right, execution weak. Record `rewrite_reason` and what
  specifically changes.
- **`consolidate`** — ≥2 URLs compete. Nominate the canonical URL, list the
  merge sources, and note that the redirect instruction is routed **through A06**
  as a `technical_issue` (A06 owns the URL graph, not A07).
- **`build_new`** — only with a written reason why no existing URL can serve the
  intent.

## Step 4 — Preserve what works

A rewrite brief must state what **not** to change: sections already performing,
existing inbound internal links, the URL itself (never change a ranking URL
without a redirect instruction), and any first-hand material already on the page.

Destroying a visit-backed section in a rewrite destroys moat. Flag any such
section `preserve: true`.

## Output
The `decision`, `existing_url`, `rewrite_reason`, `consolidation_targets`, and
`preserve` fields of the Content Brief.
