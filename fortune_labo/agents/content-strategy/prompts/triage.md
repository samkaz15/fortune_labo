# Prompt — Opportunity Triage

## Task
Resolve one inbound SEO Opportunity into exactly one decision.

## Input
`seo_opportunity.json` (+ the A06 SEO requirement set and keyword register entry).

## Step 0 — Intake validation (reject before triaging)

Return the opportunity unprocessed if any hold:

- `moat_alignment: conflicting` → route to A01 Strategy. Not yours.
- `compliance_flags` non-empty → route to A30 Compliance/Risk first.
- `tier` missing, or Tier D present.
- `evidence` empty or `evidence_confidence` absent.

Log the rejection. Do not silently fix the input.

## Step 1 — Search before you build

Query the published URL inventory and `content/briefs/` for the primary keyword,
its cluster, and near-synonyms. **You must do this before choosing `build_new`.**

## Step 2 — Choose the decision

| Decision | Condition |
| --- | --- |
| `rewrite` | An existing URL targets this intent. **Default.** Requires `existing_url` + `rewrite_reason`. |
| `consolidate` | ≥2 URLs compete for one intent. Requires `consolidation_targets`. |
| `refresh_only` | Structure sound, facts time-expired. |
| `build_new` | No existing URL can serve the intent — state why. |
| `decline` | See step 3. |

## Step 3 — Decline tests, in order

Stop at the first that fires and emit a Decline Record:

1. **One-line test** — an AI-only competitor could produce this tomorrow →
   `fails_one_line_test`
2. **Winnability** — SERP owned by shrine official sites, national media, or a
   map pack where we would be indistinguishable → `not_winnable`
3. **Positioning** — commodity theme, ranking/comparison content, or off-practice
   → `off_positioning`
4. **Source material** — no visit, no judgment, no consented client story, and
   none obtainable in the window → `no_source_material`
5. **Cluster readiness** — a spoke with no live hub → `cluster_not_ready`
6. **Capacity** — the calendar is already at stated capacity → `over_capacity`
7. **Duplication** — an existing brief or URL already serves this →
   `duplicate_of_existing`
8. **Compliance** — the theme cannot be treated without a forbidden framing →
   `compliance_risk`

Every decline carries a `revisit_condition`. A decline is a judgment under
current conditions, never a permanent verdict.

## Output
Either a decision object that feeds the brief prompt, or
`schemas/decline_record.schema.json`.
