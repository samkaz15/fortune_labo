# Prompt — Content Brief Generation

## Task
Convert a triaged opportunity into a complete Content Brief for A08.

**Precondition:** triage returned `build_new`, `rewrite`, `consolidate`, or
`refresh_only`. If it returned `decline`, stop — you emit a Decline Record, not a
brief.

## Step 1 — Source-material gate (do this before writing anything)

| Content type | Required record | If missing |
| --- | --- | --- |
| `shrine_visit_report` | `visit_record_id` (notes + photos in repo) | **Defer.** Emit a material request. |
| `annual_outlook`, `forecast_review` | `practitioner_input_id` with divinatory basis | **Defer.** |
| `case_reflection` | `practitioner_input_id` + recorded consent | **Defer.** |
| others | listed, checkable research sources | Gather first |

Do not write an outline that assumes material will arrive. That is the single
most damaging thing this agent can do.

## Step 2 — Audience

- `target_persona` — who they are, what situation they are in
- `reader_state` — what is true at the moment they type the query: what they
  already know, what they fear, what they will do next
- `persona_source` — `client_questions` / `persona_agent` / `research_agent` /
  `serp_paa`. **Mandatory.** Client questions outrank everything else.

## Step 3 — Purpose

- `content_goal` — the business outcome (e.g. "route 対面鑑定 intent in 関西 to the
  booking page")
- `content_intent` — `answer` / `orient` / `decide` / `trust` / `act` / `record`

Check the pair against `search_intent`. A `transactional` query served by an
`orient` page ranks and never converts.

## Step 4 — Angle and unique value

Write `unique_value` in one sentence, then apply the one-line test and record the
result in `differentiation_basis`.

Acceptable bases: a first-hand visit; the practitioner's stated judgment with its
divinatory basis; a synthesis of real client questions; a local detail obtainable
only by being there.

Not acceptable: "more comprehensive", "better structured", "more current".

## Step 5 — Titles

3+ candidates, each ≤ 60 characters, primary keyword natural in each.

Screen every candidate against `../rules.md` §4:

| Reject | Because |
| --- | --- |
| `行かないと運気が下がる` | fear framing |
| `願いが叶う神社` | guaranteed outcome |
| `効く神社ランキング` | efficacy ranking |
| `金運が上がる` | implied financial outcome |

"Visiting is good" is permitted. "Not visiting is bad" is not.
**You own titles, so a fear-framed title is your violation, not A08's.**

## Step 6 — Outline

Per H2/H3 section:

| Field | Note |
| --- | --- |
| `heading_level` | `h2` / `h3` |
| `heading` | |
| `purpose` | What the reader gains. "Explain the background" is not a purpose. |
| `target_question` | The reader question this section answers |
| `source_requirement` | `visit_notes` / `practitioner_judgment` / `research` / `ai_structurable` |
| `featured_snippet_target` | At most one per brief |

Count `ai_structurable` sections. Over 50% ⇒ set `low_moat_density: true` and
reconsider the whole brief.

## Step 7 — Distribution

- **CTA:** exactly one primary. Match it to `reader_state` — a first-contact,
  high-anxiety reader gets `list_signup`, not `booking`. No urgency-through-fear
  in `copy_direction`.
- **Internal links:** ≥1 planned inbound (zero = orphan = rejected), cluster hub
  outbound, and the booking page outbound for Tier A/B.
- **`sns_repurpose`:** per channel, one of `strong` / `possible` / `skip`, with
  `angle`, `objective`, `rationale`. `skip` is a normal answer — a shrine report
  with no usable photography is not an Instagram post.

## Step 8 — Governance

Set `compliance_requirements`: disclaimer, subjectivity marking, divinatory basis
(mandatory for `annual_outlook`), photo permission status, and any
`sensitive_domain` flag (medical / financial / legal / major life decision) which
routes the brief to A30 before drafting.

Set `priority` and `publish_by` (backward-planned from A06's seasonal window).

## Step 9 — Capacity check

```
if committed_capacity + this_brief > practitioner_monthly_capacity:
        DO NOT ISSUE
        escalate to A01 Strategy with a proposed cut list
```

## Output
`schemas/content_brief.schema.json`, written to `content/briefs/CB-xxxx.json`.
